from datetime import datetime
from django.core.management.base import BaseCommand, CommandError

import os
import pandas as pd

from dashboard.settings import USER_DATA_PATH, CONSUMPTION_DATA_DIR
from consumption.models import User, Consumption, ConsumptionRollup


class Command(BaseCommand):
    help = 'import data'

    def add_arguments(self, parser):
        parser.add_argument('user_data_path', nargs='?', type=str)
        parser.add_argument('consumption_data_dir', nargs='?', type=str)

    def handle(self, *args, **options):
        start_time = datetime.now()

        self.import_users(options['user_data_path'])
        self.import_consumptions(options['consumption_data_dir'])

        self.stdout.write('Recalculating consumption aggregate data')
        ConsumptionRollup.full_recalc()

        self.stdout.write('Import complete. Duration: %s' % (datetime.now() - start_time))

    def import_users(self, user_data_path=None):
        if user_data_path is None:
            user_data_path = USER_DATA_PATH

        if not os.path.exists(user_data_path):
            raise CommandError('The following path does not exist: %s' % user_data_path)

        self.stdout.write('Importing user data from %s' % user_data_path)
        User.objects.all().delete()

        df = pd.read_csv(user_data_path)

        User.objects.bulk_create(
            User(**vals) for vals in df.to_dict('records')
        )

    def import_consumptions(self, consumption_data_dir=None):
        if consumption_data_dir is None:
            consumption_data_dir = CONSUMPTION_DATA_DIR

        if not os.path.exists(consumption_data_dir):
            raise CommandError('The following path does not exist: %s' % consumption_data_dir)

        Consumption.objects.all().delete()

        for user in User.objects.all():
            data_path = os.path.join(consumption_data_dir, '%s.csv' % user.pk)

            self.stdout.write('Importing consumption data from %s' % data_path)

            if not os.path.exists(data_path):
                continue

            df = pd.read_csv(data_path)
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['user_id'] = user.pk
            df = df.drop_duplicates(subset='datetime')

            Consumption.objects.bulk_create(
                Consumption(**vals) for vals in df.to_dict('records')
            )
