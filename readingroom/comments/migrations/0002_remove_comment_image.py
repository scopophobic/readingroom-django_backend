# Generated by Django 5.2 on 2025-05-13 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comments", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="image",
        ),
    ]
