# Generated by Django 4.1.7 on 2023-03-04 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_register', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_name',
            new_name='name',
        ),
    ]
