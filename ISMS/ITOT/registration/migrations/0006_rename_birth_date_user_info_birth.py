# Generated by Django 4.0.2 on 2022-02-10 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_rename_dob_user_info_birth_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='Birth_Date',
            new_name='birth',
        ),
    ]