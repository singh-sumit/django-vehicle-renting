# Generated by Django 3.2.6 on 2021-08-14 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0015_reservation_reservationrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='submit_date',
            new_name='retun_date',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='submit_approver',
            new_name='return_approver',
        ),
    ]
