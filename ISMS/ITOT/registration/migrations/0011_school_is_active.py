# Generated by Django 4.0.2 on 2022-02-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_alter_applications_role_alter_applications_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
