# -*- coding: utf-8 -*-

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
