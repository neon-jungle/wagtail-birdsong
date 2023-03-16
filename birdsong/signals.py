from datetime import timedelta, date

from django.db.models.signals import post_save
from django.dispatch import receiver


from birdsong.models import Campaign, Contact, BirdsongSettings


@receiver(post_save, sender=Campaign)
def clean_unconfirmed_contacts(sender, instance, created, **kwargs):
    birdsong_settings = BirdsongSettings.load()
    if birdsong_settings.double_opt_in_enabled:
        Contact.objects.filter(
            created_at__lt=date.today() - timedelta(weeks=1), is_confirmed=False
        ).delete()
