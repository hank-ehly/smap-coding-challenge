import pytz
from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime

from consumption.models import User, Consumption


class DetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(area='a1', tariff='t1')

        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 00, 0, tzinfo=pytz.UTC), consumption=100)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 0, 30, 0, tzinfo=pytz.UTC), consumption=200)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 00, 0, tzinfo=pytz.UTC), consumption=300)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 1, 30, 0, tzinfo=pytz.UTC), consumption=400)
        Consumption.objects.create(user=user, datetime=datetime(2016, 7, 15, 2, 00, 0, tzinfo=pytz.UTC), consumption=500)

    def setUp(self):
        self.user = User.objects.first()

    def test_non_existent_user(self):
        response = self.client.get(reverse('consumption:detail', args=(9999999,)))
        self.assertEqual(response.status_code, 404)

    def test_existing_user(self):
        response = self.client.get(reverse('consumption:detail', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User %s Details' % self.user.id)
