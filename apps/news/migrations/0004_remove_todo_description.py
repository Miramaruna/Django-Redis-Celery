# Generated by Django 5.1.2 on 2025-02-06 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='description',
        ),
    ]
