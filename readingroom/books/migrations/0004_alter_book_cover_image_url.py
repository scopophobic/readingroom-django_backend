# Generated by Django 5.2 on 2025-05-07 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0003_alter_book_authors_alter_book_isbn_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="cover_image_url",
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
