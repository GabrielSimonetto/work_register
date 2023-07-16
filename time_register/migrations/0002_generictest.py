# Generated by Django 4.1.7 on 2023-07-13 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("time_register", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GenericTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField()),
                ("resource", models.TextField()),
            ],
        ),
    ]
