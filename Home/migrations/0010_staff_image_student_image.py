# Generated by Django 4.2 on 2023-05-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Home", "0009_rename_role_staff_department"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="staff_images/"),
        ),
        migrations.AddField(
            model_name="student",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="student_images/"),
        ),
    ]
