from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, date

from .models import Campaign, Contact


@receiver(post_save)
def clean_unconfirmed_contacts(sender, instance, created, **kwargs):
    if issubclass(sender, Campaign):
        Contact.objects.filter(
            created_at__lt=date.today() - timedelta(weeks=1)
        ).delete()
