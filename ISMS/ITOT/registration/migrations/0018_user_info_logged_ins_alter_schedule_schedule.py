# Generated by Django 4.0.2 on 2022-02-18 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0017_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='logged_ins',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 18, 11, 6, 47, 273715)),
        ),
    ]
