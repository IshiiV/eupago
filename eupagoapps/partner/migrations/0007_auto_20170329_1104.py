# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-29 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20170329_1032'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockrecord',
            unique_together=set([]),
        ),
    ]