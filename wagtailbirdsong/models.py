from django.conf import settings
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.utils import camelcase_to_underscore
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .blocks import DefaultBlocks
from .backends import BaseEmailBackend


class Campaign(models.Model):
    subject = models.TextField()

    panels = [
        FieldPanel('subject'),
    ]

    def get_template(self, request):
        return "%s/mail/%s.html" % (self._meta.app_label, camelcase_to_underscore(self.__class__.__name__))
    
    def get_backend(self):
        return BaseEmailBackend
    
    def get_contact_model(self):
        return BaseContact
    
    def get_from_email(self):
        if hasattr(settings, 'WAGTAILBIRDSONG_FROM_EMAIL'):
            return settings.WAGTAILBIRDSONG_FROM_EMAIL
        return settings.DEFAULT_FROM_EMAIL


class Contact(models.Model):
    email = models.EmailField()


class Receipt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='receipts')
    recipient_fk = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='recipient_fk')
    sent_date = models.DateTimeField(blank=True)

    @property
    def recipient(self):
        # Can't use a OneToOneField because receipts can be made for the same contact across multiple campaigns
        return self.recipient_fk.objects.first()

    @property
    def success(self):
        return self.sent_date
