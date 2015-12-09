# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='type',
            field=models.CharField(default='Normal', max_length=10),
            preserve_default=False,
        ),
    ]
