from django.apps import AppConfig


class WagtailBirdsongApp(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "birdsong"
    label = "birdsong"
    verbose_name = "Wagtail Birdsong"

    def ready(self):
        from . import signals  # noqa
