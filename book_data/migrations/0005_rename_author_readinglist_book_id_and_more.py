# Generated by Django 5.1.2 on 2025-02-18 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book_data", "0004_remove_reviews_data_time_reviews_review_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="readinglist",
            old_name="author",
            new_name="book_id",
        ),
        migrations.RemoveField(
            model_name="readinglist",
            name="open_library_id",
        ),
    ]
