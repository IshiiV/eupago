# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-28 21:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_remove_stockrecord_bid4'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockrecord',
            unique_together=set([]),
        ),
    ]
