# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.CharField(max_length=200)),
                ('dayOfWeek', models.CharField(max_length=20)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('room', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=200)),
                ('course', models.ForeignKey(to='main.Course')),
                ('lessonType', models.ForeignKey(to='main.LessonType')),
                ('period', models.ManyToManyField(to='main.Period')),
            ],
        ),
    ]
