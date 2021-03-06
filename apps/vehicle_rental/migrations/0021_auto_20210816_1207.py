# Generated by Django 3.2.6 on 2021-08-16 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle_rental', '0020_alter_reservation_expected_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationrequest',
            name='status',
            field=models.CharField(choices=[('INPROGESS', 'INPROGRESS'), ('GRANTED', 'GRANTED'), ('DENIED', 'DENIED'), ('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED')], default='INPROGRESS', max_length=50),
        ),
        migrations.CreateModel(
            name='InstantIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_prepayment', models.FloatField()),
                ('earned_fine', models.FloatField(default=0)),
                ('earned_total', models.FloatField()),
                ('date_updated', models.DateField(auto_now=True)),
                ('reserv_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vehicle_rental.reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
