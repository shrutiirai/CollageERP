# Generated by Django 4.1.7 on 2023-05-09 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='role',
            new_name='department',
        ),
    ]
