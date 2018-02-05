# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDay
from django.utils.encoding import python_2_unicode_compatible

import pandas as pd


@python_2_unicode_compatible
class User(models.Model):
    area = models.CharField(max_length=2)
    tariff = models.CharField(max_length=2)

    def __str__(self):
        return self.pk

    def consumptions(self):
        query_set = Consumption.objects \
            .filter(user_id=self.pk) \
            .annotate(date=TruncDay('datetime')) \
            .values('date') \
            .annotate(sum=Sum('consumption'))


@python_2_unicode_compatible
class Consumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Time of consumption')
    consumption = models.FloatField()

    def __str__(self):
        return "%s (user=%s)" % (self.pk, self.user.id)

    class Meta:
        unique_together = (('user', 'datetime'),)


@python_2_unicode_compatible
class ConsumptionRollup(models.Model):
    date = models.DateField('Date of consumption')
    average = models.IntegerField(default=0)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return '%s (avg=%s, sum=%s)' % (self.date, self.average, self.sum)

    @staticmethod
    def full_recalc():
        ConsumptionRollup.objects.all().delete()

        query_set = Consumption.objects \
            .annotate(date=TruncDay('datetime')) \
            .values('date') \
            .annotate(sum=Sum('consumption')) \
            .annotate(average=Avg('consumption'))

        df = pd.DataFrame(list(query_set))

        ConsumptionRollup.objects.bulk_create(
            ConsumptionRollup(**vals) for vals in df.to_dict('records')
        )
