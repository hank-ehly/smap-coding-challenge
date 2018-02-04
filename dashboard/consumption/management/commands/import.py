from django.core.management.base import BaseCommand

import pandas as pd

from dashboard.settings import USER_DATA_PATH
from consumption.models import User


def import_users(user_data_path=USER_DATA_PATH):
    df = pd.read_csv(user_data_path)

    User.objects.bulk_create(
        User(**vals) for vals in df.to_dict('records')
    )


class Command(BaseCommand):
    help = 'import data'

    def handle(self, *args, **options):
        import_users()
