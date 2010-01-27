# -*- coding: utf-8 -*-

from django.test import TestCase

from people.models import Person


class SimpleTest(TestCase):
    
    fixtures = ['testing']
    
    def test_basic(self):
        self.failUnlessEqual(
            pks(Person.men),
            pks(Person.objects.filter(gender='m')))
        
        self.failUnlessEqual(
            pks(Person.women),
            pks(Person.objects.filter(gender='f')))
        
        self.failUnlessEqual(
            pks(Person.minors),
            pks(Person.objects.filter(age__lt=18)))
    
    def test_composite_1(self):
        self.failUnlessEqual(
            pks(Person.specified),
            pks(Person.objects.filter(gender__in=['m', 'f'])))
        
        self.failUnlessEqual(
            pks(Person.adults),
            pks(Person.objects.filter(age__gte=18)))
    
    def test_composite_2(self):
        self.failUnlessEqual(
            pks(Person.unspecified),
            pks(Person.objects.filter(gender='u')))


def pks(qset):
    """Return the list of primary keys for the results of a QuerySet."""
    
    return sorted(tuple(qset.values_list('pk', flat=True)))
