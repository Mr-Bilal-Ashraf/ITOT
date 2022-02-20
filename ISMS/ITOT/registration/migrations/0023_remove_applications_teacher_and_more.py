# Generated by Django 4.0.2 on 2022-02-19 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0022_alter_schedule_schedule_teachers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='students',
            name='registered_by',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 19, 14, 25, 5, 288814)),
        ),
        migrations.DeleteModel(
            name='Teachers',
        ),
    ]
