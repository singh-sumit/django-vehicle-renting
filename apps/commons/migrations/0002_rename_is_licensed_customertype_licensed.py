# Generated by Django 3.2.6 on 2021-08-09 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customertype',
            old_name='is_licensed',
            new_name='licensed',
        ),
    ]
