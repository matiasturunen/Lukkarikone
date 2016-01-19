# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151112_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='dayOfWeek',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
