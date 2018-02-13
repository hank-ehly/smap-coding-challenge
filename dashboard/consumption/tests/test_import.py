# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.test import TestCase
from django.core.management import call_command, CommandError
from django.utils.six import StringIO

from consumption.models import User, Consumption
from dashboard.settings import BASE_DIR


class ImportTest(TestCase):

    def setUp(self):
        fixtures_dir = os.path.join(BASE_DIR, 'consumption', 'tests', 'fixtures')
        self.test_user_data_path = os.path.join(fixtures_dir, 'user_data.csv')
        self.test_consumption_data_dir = os.path.join(fixtures_dir, 'consumption')
        self.dup_consumption_data_dir = os.path.join(fixtures_dir, 'duplicate_consumption')
        self.out = StringIO()

    def test_import_user_data(self):
        call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir=self.test_consumption_data_dir, stdout=self.out)
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_import_consumption_data(self):
        call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir=self.test_consumption_data_dir, stdout=self.out)
        consumption_count = Consumption.objects.count()
        self.assertEqual(consumption_count, 200)

    def test_non_existent_user_data_path(self):
        with self.assertRaises(CommandError) as ctx:
            call_command('import', user_data_path='/xyz', consumption_data_dir=self.test_consumption_data_dir, stdout=self.out)
        self.assertEqual('The following path does not exist: /xyz', str(ctx.exception))

    def test_non_existent_consumption_data_dir(self):
        with self.assertRaises(CommandError) as ctx:
            call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir='/foo', stdout=self.out)
        self.assertEqual('The following path does not exist: /foo', str(ctx.exception))

    def test_duplicate_datetime(self):
        call_command('import', user_data_path=self.test_user_data_path, consumption_data_dir=self.dup_consumption_data_dir, stdout=self.out)

        dup_filter = Consumption.objects.filter(user_id=3000).filter(datetime='2016-07-15 00:00:00')
        self.assertEqual(dup_filter.count(), 1)
        self.assertEqual(dup_filter.first().consumption, 1000)

        dup_entry_count = Consumption.objects.filter(user_id=3000).filter(consumption=9999).count()
        self.assertEqual(dup_entry_count, 0)

