# Generated by Django 3.2.6 on 2021-08-16 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0021_auto_20210816_1207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instantincome',
            old_name='reserv_id',
            new_name='reserv',
        ),
    ]