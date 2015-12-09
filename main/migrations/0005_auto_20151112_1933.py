# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151112_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(to='main.Course', null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='dayOfWeek',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='endTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='room',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='startTime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='week',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
