# Generated by Django 3.2.6 on 2021-08-14 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0018_auto_20210814_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='return_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
