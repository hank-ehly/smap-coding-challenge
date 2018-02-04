# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class User(models.Model):
    area = models.CharField(max_length=2)
    tariff = models.CharField(max_length=2)

    def __str__(self):
        return self.pk


@python_2_unicode_compatible
class Consumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Time of consumption')
    consumption = models.FloatField()

    def __str__(self):
        return "%s (user=%s)" % (self.pk, self.user.id)
