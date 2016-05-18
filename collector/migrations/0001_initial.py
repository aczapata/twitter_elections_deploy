# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=11, decimal_places=7)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('source', models.CharField(max_length=250, null=True, blank=True)),
                ('user', models.CharField(max_length=300, null=True)),
                ('user_location', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
    ]
