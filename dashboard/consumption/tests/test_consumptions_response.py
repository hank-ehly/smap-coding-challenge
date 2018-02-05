import pytz
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
import json

from consumption.models import User, Consumption, ConsumptionRollup


class ConsumptionsResponseTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(area='a1', tariff='t1')
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 00, 0, tzinfo=pytz.UTC), consumption=100)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), consumption=200)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 00, 0, tzinfo=pytz.UTC), consumption=300)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 30, 0, tzinfo=pytz.UTC), consumption=400)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 2, 00, 0, tzinfo=pytz.UTC), consumption=500)
        ConsumptionRollup.full_recalc()

    def test_status_code(self):
        response = self.client.get(reverse('consumption:consumptions'))
        self.assertEqual(response.status_code, 200)

    def test_without_data(self):
        ConsumptionRollup.objects.all().delete()
        response = self.client.get(reverse('consumption:consumptions'))
        json_body = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json_body, [])

    def test_with_data(self):
        response = self.client.get(reverse('consumption:consumptions'))
        json_body = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(json_body, [{
            'fields': {
                'average': 300,
                'date': '2016-07-15',
                'sum': 1500
            },
            'model': 'consumption.consumptionrollup',
            'pk': 1
        }])
