# Generated by Django 3.2.6 on 2021-08-16 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_rental', '0022_rename_reserv_id_instantincome_reserv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantincome',
            name='reserv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_rental.reservation'),
        ),
    ]
