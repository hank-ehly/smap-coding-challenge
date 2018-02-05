import pytz
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime

from consumption.models import User, Consumption


class SummaryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(area='a1', tariff='t1')

        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 00, 0, tzinfo=pytz.UTC), consumption=100)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), consumption=200)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 00, 0, tzinfo=pytz.UTC), consumption=300)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 30, 0, tzinfo=pytz.UTC), consumption=400)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 2, 00, 0, tzinfo=pytz.UTC), consumption=500)

    def test_no_data(self):
        User.objects.all().delete()

        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No users are available!')
        self.assertQuerysetEqual(response.context['user_list'], [])

    def test_with_data(self):
        response = self.client.get(reverse('consumption:summary'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Summary')
        self.assertQuerysetEqual(response.context['user_list'], ['<User: 1>'])
