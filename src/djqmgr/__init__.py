# -*- coding: utf-8 -*-

__version__ = '0.1'

from django.db import models


class QManager(models.Manager):
    
    """
    Create managers for Django models based on pre-defined queries.
    
    Basic usage is as follows:
        
        from django.db import models
        from djqmgr import QManager
        
        class Person(models.Model):
            
            GENDERS = (
                ('m', 'Male'),
                ('f', 'Female'),
                ('u', 'Unspecified'),
            )
            
            age = models.PositiveIntegerField()
            gender = models.CharField(max_length=1, choices=GENDERS)
            
            objects = models.Manager()
            
            minors = QManager(age__lt=18)
            adults = ~minors
            
            men = QManager(gender='m')
            women = QManager(gender='f')
            specified = men | women
            unspecified = ~(men | women)
    
    Note that you can invert and combine `QManager` instances as you can `Q`
    objects, and the binary *or* and *and* operators (via `|` and `&`) can
    accept other `QManager` objects, `Q` objects, and dictionaries.
    """
    
    query = None
    
    @classmethod
    def for_query(cls, query):
        """Construct a `QManager` subclass for the given query."""
        
        return type('QManager', (cls,), {'query': to_query(query)})
    
    def __new__(cls, query=None, **kwargs):
        if cls.query is not None:
            assert not (query or kwargs), "A query is already specified for this QManager"
            return models.Manager.__new__(cls)
        
        assert bool(query) ^ bool(kwargs), "Give either a query or some filter arguments"
        if query is None:
            query = kwargs
        
        return cls.for_query(query)()
    
    def __init__(self, *args, **kwargs):
        super(QManager, self).__init__()
    
    def __or__(self, other):
        return type(self).for_query(self.query | to_query(other))()
    
    def __and__(self, other):
        return type(self).for_query(self.query & to_query(other))()
    
    def __invert__(self):
        return type(self).for_query(~self.query)()
    
    def get_query_set(self, *args, **kwargs):
        return super(QManager, self).get_query_set(*args, **kwargs).filter(self.query)


def to_query(obj):
    
    """
    Coerce an arbitrary object to a `Q` instance.
    
    The scheme for conversion is as follows:
    *   `Q` instances => obj
    *   `QManager` classes => `obj.query`
    *   `QManager` instances => `type(obj).query`
    *   Everything else => `Q(**obj)`
    """
    
    if isinstance(obj, models.Q):
        return obj
    elif isinstance(obj, QManager):
        return type(obj).query
    elif isinstance(obj, type) and issubclass(obj, QManager):
        return obj.query
    return models.Q(**obj)
