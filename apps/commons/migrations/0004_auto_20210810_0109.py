# Generated by Django 3.2.6 on 2021-08-09 19:24

import apps.commons.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0003_alter_customer_license_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csr',
            name='mobile',
            field=models.PositiveIntegerField(help_text='Your mobile number', validators=[apps.commons.utils.validate_phone]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.PositiveIntegerField(help_text='Your mobile number', validators=[apps.commons.utils.validate_phone]),
        ),
        migrations.AlterField(
            model_name='owner',
            name='mobile',
            field=models.PositiveIntegerField(help_text='Your mobile number', validators=[apps.commons.utils.validate_phone]),
        ),
    ]
