# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.test import TestCase
from django.core.management import call_command

from consumption.models import User, Consumption
from dashboard.settings import BASE_DIR


class ImportTest(TestCase):

    def setUp(self):
        fixtures_dir = os.path.join(BASE_DIR, 'consumption', 'tests', 'fixtures')
        self.test_user_data_path = os.path.join(fixtures_dir, 'user_data.csv')
        self.test_consumption_data_dir = os.path.join(fixtures_dir, 'consumption')

    def test_import_user_data(self):
        call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir=self.test_consumption_data_dir)
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_import_consumption_data(self):
        call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir=self.test_consumption_data_dir)
        consumption_count = Consumption.objects.count()
        self.assertEqual(consumption_count, 200)
