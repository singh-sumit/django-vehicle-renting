# Generated by Django 3.2.6 on 2021-08-09 19:27

import apps.commons.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0004_auto_20210810_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csr',
            name='mobile',
            field=models.PositiveIntegerField(validators=[apps.commons.utils.validate_phone]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.PositiveIntegerField(validators=[apps.commons.utils.validate_phone]),
        ),
        migrations.AlterField(
            model_name='owner',
            name='mobile',
            field=models.PositiveIntegerField(validators=[apps.commons.utils.validate_phone]),
        ),
    ]
