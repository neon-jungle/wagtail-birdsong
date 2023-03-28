from django.apps import AppConfig
from django.db.models.signals import post_save



class WagtailBirdsongApp(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'birdsong'
    label = 'birdsong'
    verbose_name = 'Wagtail Birdsong'

    def ready(self):
        from .signals import clean_unconfirmed_contacts
        from .models import Campaign
        for subclass in Campaign.__subclasses__():
            post_save.connect(clean_unconfirmed_contacts, sender=subclass)
