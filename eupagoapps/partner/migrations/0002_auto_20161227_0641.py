# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-27 08:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import oscar.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ('name', 'code'), 'permissions': (('dashboard_access', 'Can access dashboard'),), 'verbose_name': 'Fulfillment partner', 'verbose_name_plural': 'Fulfillment partners'},
        ),
        migrations.AddField(
            model_name='stockrecord',
            name='bid1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Bid 1'),
        ),
        migrations.AddField(
            model_name='stockrecord',
            name='bid2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Bid 2'),
        ),
        migrations.AddField(
            model_name='stockrecord',
            name='bid3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Bid 3'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='partners', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='stockrecord',
            name='price_currency',
            field=models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='Currency'),
        ),
    ]
