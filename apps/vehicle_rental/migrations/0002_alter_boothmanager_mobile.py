# Generated by Django 3.2.6 on 2021-08-09 19:24

import apps.commons.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boothmanager',
            name='mobile',
            field=models.PositiveIntegerField(help_text='Your mobile number', validators=[apps.commons.utils.validate_phone]),
        ),
    ]
