# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_match_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='group',
            field=models.CharField(max_length=20, null=True),
        ),
    ]