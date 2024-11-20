# Generated by Django 5.1.1 on 2024-11-20 19:14

import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                default=django.utils.timezone.now,
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
            preserve_default=False,
        ),
    ]
