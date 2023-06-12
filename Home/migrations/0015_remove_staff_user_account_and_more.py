# Generated by Django 4.2 on 2023-05-18 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Home", "0014_staff_user_account_student_user_account"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staff",
            name="user_account",
        ),
        migrations.RemoveField(
            model_name="student",
            name="user_account",
        ),
        migrations.AddField(
            model_name="staff",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
