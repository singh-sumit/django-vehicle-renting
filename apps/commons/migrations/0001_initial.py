# Generated by Django 3.2.6 on 2021-08-09 15:36

import apps.commons.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CSR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm_address', models.CharField(help_text='Enter your permanent address', max_length=50)),
                ('curr_address', models.CharField(help_text='Enter your current address', max_length=50)),
                ('mobile', models.PositiveIntegerField(help_text='Your mobile number', validators=[django.core.validators.MinLengthValidator(10), apps.commons.utils.validate_phone])),
                ('salary', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm_address', models.CharField(help_text='Enter your permanent address', max_length=50)),
                ('curr_address', models.CharField(help_text='Enter your current address', max_length=50)),
                ('mobile', models.PositiveIntegerField(help_text='Your mobile number', validators=[django.core.validators.MinLengthValidator(10), apps.commons.utils.validate_phone])),
                ('dob', models.DateField()),
                ('license_doc', models.ImageField(upload_to='licenses')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm_address', models.CharField(help_text='Enter your permanent address', max_length=50)),
                ('curr_address', models.CharField(help_text='Enter your current address', max_length=50)),
                ('mobile', models.PositiveIntegerField(help_text='Your mobile number', validators=[django.core.validators.MinLengthValidator(10), apps.commons.utils.validate_phone])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_licensed', models.BooleanField(default=False)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='commons.customer')),
                ('verifier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='commons.csr')),
            ],
        ),
    ]
