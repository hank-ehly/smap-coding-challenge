from datetime import datetime
from django.core.management.base import BaseCommand

import os
import pandas as pd

from dashboard.settings import USER_DATA_PATH, CONSUMPTION_DATA_DIR
from consumption.models import User, Consumption


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])

        start_time = datetime.now()
        self.stdout.write('Started import at %s' % start_time)

        self.import_users()
        self.import_consumptions()

        import_duration = datetime.now() - start_time
        self.stdout.write('Import complete. Duration: %s' % import_duration)

    def import_users(self, user_data_path=USER_DATA_PATH):
        self.stdout.write('Importing user data.')

        User.objects.all().delete()

        df = pd.read_csv(user_data_path)

        User.objects.bulk_create(
            User(**vals) for vals in df.to_dict('records')
        )

    def import_consumptions(self, consumption_data_dir=CONSUMPTION_DATA_DIR):
        Consumption.objects.all().delete()

        for user in User.objects.all():
            self.stdout.write('Importing consumption data for User %s' % user.pk)

            data_path = os.path.join(consumption_data_dir, '%s.csv' % user.pk)

            df = pd.read_csv(data_path)
            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['user_id'] = user.pk

            Consumption.objects.bulk_create(
                Consumption(**vals) for vals in df.to_dict('records')
            )
