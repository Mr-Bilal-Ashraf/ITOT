# Generated by Django 4.0.2 on 2022-02-19 07:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0019_alter_applications_school_alter_schedule_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 19, 12, 28, 41, 875444)),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
