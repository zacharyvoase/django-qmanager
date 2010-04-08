# `django-qmanager`

`django-qmanager` is a reusable Django application which allows you to create managers for Django models, based on pre-defined queries. It leverages Django's `Q` object (`django.db.models.Q`) to allow for rich expressions, without having to go through the rigmarole of sub-classing `django.db.models.Manager` and overriding `get_query_set()`. Easy things should be easy.

## Installation

The usual:

    easy_install django-qmanager # OR
    pip install django-qmanager

The only other thing you'll need is Django itself.

## Usage

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

Note that you can invert and combine `QManager` instances as you can `Q` objects, and the binary *or* and *and* operators (via `|` and `&`) can accept other `QManager` objects, `Q` objects, and dictionaries.

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
