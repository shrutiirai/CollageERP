# Generated by Django 4.2 on 2023-06-09 13:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Home", "0023_alter_attendance_unique_together"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Exam",
        ),
    ]
