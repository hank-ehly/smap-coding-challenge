# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.test import TestCase
from django.core.management import call_command

from consumption.models import User, Consumption
from dashboard.settings import BASE_DIR

FIXTURES_DIR = os.path.join(BASE_DIR, 'consumption', 'tests', 'fixtures')
TEST_USER_DATA_PATH = os.path.join(FIXTURES_DIR, 'user_data.csv')
TEST_CONSUMPTION_DATA_DIR = os.path.join(FIXTURES_DIR, 'consumption')


class ImportTest(TestCase):

    def test_import_user_data(self):
        call_command('import', user_data_path=TEST_USER_DATA_PATH, consumption_data_dir=TEST_CONSUMPTION_DATA_DIR)
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_import_consumption_data(self):
        call_command('import', user_data_path=TEST_USER_DATA_PATH, consumption_data_dir=TEST_CONSUMPTION_DATA_DIR)
        consumption_count = Consumption.objects.count()
        self.assertEqual(consumption_count, 200)
