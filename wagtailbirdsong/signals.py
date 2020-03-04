from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Contact
from .backends import sendgrid

@receiver(post_save, sender=Contact)
def contact_updated(sender, instance, created, **kwargs):
    sendgrid.subscribe_user(instance)

@receiver(post_delete, sender=Contact)
def contact_deleted(sender, instance, **kwargs):
    sendgrid.unsubscribe_user(instance)

