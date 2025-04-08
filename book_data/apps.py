from django.apps import AppConfig


class BookDataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book_data"

    def ready(self):
        import book_data.signals