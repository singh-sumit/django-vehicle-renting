# Generated by Django 3.2.6 on 2021-08-14 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0017_rename_retun_date_reservation_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='expected_return_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='borrow_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
