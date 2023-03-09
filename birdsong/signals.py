from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, date

from birdsong.models import Campaign, Contact, DoubleOptInSettings


@receiver(post_save, sender=Campaign)
def clean_unconfirmed_contacts(sender, instance, created, **kwargs):
    doi_settings = DoubleOptInSettings.load()
    if issubclass(sender, Campaign) & doi_settings.double_opt_in_enabled == True:
        Contact.objects.filter(
            created_at__lt=date.today() - timedelta(weeks=1), is_confirmed=False
        ).delete()
