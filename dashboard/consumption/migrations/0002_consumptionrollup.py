# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionRollup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sum', models.IntegerField()),
                ('average', models.IntegerField())
            ],
        ),
    ]
