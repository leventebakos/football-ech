# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_match_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='away_team',
            field=models.CharField(choices=[('AL', 'Albania'), ('AT', 'Austria'), ('BE', 'Belgium'), ('HR', 'Croatia'), ('CZ', 'Czech'), ('EN', 'England'), ('FR', 'France'), ('DE', 'Germany'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IT', 'Italy'), ('NI', 'N. Ireland'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RI', 'R. of Ireland'), ('RO', 'Romania'), ('RU', 'Russia'), ('SK', 'Slovakia'), ('SP', 'Spain'), ('SE', 'Sweden'), ('SW', 'Switzerland'), ('TK', 'Turkey'), ('UK', 'Ukraine'), ('WA', 'Wales')], max_length=2),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_team',
            field=models.CharField(choices=[('AL', 'Albania'), ('AT', 'Austria'), ('BE', 'Belgium'), ('HR', 'Croatia'), ('CZ', 'Czech'), ('EN', 'England'), ('FR', 'France'), ('DE', 'Germany'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IT', 'Italy'), ('NI', 'N. Ireland'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RI', 'R. of Ireland'), ('RO', 'Romania'), ('RU', 'Russia'), ('SK', 'Slovakia'), ('SP', 'Spain'), ('SE', 'Sweden'), ('SW', 'Switzerland'), ('TK', 'Turkey'), ('UK', 'Ukraine'), ('WA', 'Wales')], max_length=2),
        ),
    ]