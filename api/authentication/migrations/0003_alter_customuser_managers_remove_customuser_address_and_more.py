# Generated by Django 5.1.1 on 2024-11-20 20:06

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_alter_customuser_managers_customuser_username"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customuser",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="address",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="contact_number",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="name",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(max_length=20),
        ),
    ]
