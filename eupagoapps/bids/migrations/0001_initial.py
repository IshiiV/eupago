# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-02 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('u2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('u3', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
