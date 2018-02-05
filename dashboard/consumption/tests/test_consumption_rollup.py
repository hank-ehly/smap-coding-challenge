from datetime import datetime
from django.test import TestCase
import pytz

from consumption.models import Consumption, ConsumptionRollup, User


class ConsumptionRollupTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(area='a1', tariff='t1')

        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 00, 0,tzinfo=pytz.UTC), consumption=100)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 30, 0,tzinfo=pytz.UTC), consumption=200)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 00, 0,tzinfo=pytz.UTC), consumption=300)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 30, 0,tzinfo=pytz.UTC), consumption=400)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 2, 00, 0,tzinfo=pytz.UTC), consumption=500)

    def test_full_recalc_trunc_date(self):
        ConsumptionRollup.full_recalc()
        self.assertEqual(ConsumptionRollup.objects.count(), 1)

    def test_full_recalc_calculates_avg(self):
        ConsumptionRollup.full_recalc()
        self.assertEqual(ConsumptionRollup.objects.first().average, 300)
