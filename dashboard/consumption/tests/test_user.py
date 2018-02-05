import pytz
from django.test import TestCase
from django.utils.datetime_safe import datetime

from consumption.models import User, Consumption


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(area='a1', tariff='t1')

        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 00, 0, tzinfo=pytz.UTC), consumption=100)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), consumption=200)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 00, 0, tzinfo=pytz.UTC), consumption=300)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 30, 0, tzinfo=pytz.UTC), consumption=400)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 2, 00, 0, tzinfo=pytz.UTC), consumption=500)

    def setUp(self):
        user = User.objects.first()
        consumptions = user.consumptions()
        self.consumption = consumptions[0]

    def test_consumptions_contains_correct_date(self):
        self.assertEqual(self.consumption['date'], datetime(2016, 7, 15, 0, 0, tzinfo=pytz.UTC))

    def test_consumptions_contains_correct_sum(self):
        self.assertEqual(self.consumption['sum'], 1500)  # 100 + 200 + 300 + 400 + 500

    def test_consumptions_contains_correct_average(self):
        self.assertEqual(self.consumption['average'], 300)  # (100 + 200 + 300 + 400 + 500) / 5
