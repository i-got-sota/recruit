# Generated by Django 4.2.1 on 2023-05-07 12:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_user_nickname"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_id",
            field=models.CharField(
                max_length=20,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator("^[a-zA-Z0-9]+$"),
                    django.core.validators.MinLengthValidator(6),
                ],
            ),
        ),
    ]
