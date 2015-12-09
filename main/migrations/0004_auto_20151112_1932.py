# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_period_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, to='main.Course'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='dayOfWeek',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='endTime',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='room',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='startTime',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='week',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
