# Generated by Django 4.0.2 on 2022-02-07 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfCode',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Con_code', models.CharField(blank=True, max_length=6, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='Con_code',
        ),
    ]
