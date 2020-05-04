from django.conf import settings
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.utils import camelcase_to_underscore
from wagtail.contrib.settings.models import BaseSetting, register_setting

from .blocks import DefaultBlocks
from .backends import BaseEmailBackend


class Contact(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email



class Campaign(models.Model):
    name = models.CharField(
        max_length=255, help_text='The name of the campaign')
    subject = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)
    receipts = models.ManyToManyField(Contact, through='Receipt')

    panels = [
        FieldPanel('name'),
        FieldPanel('subject'),
    ]

    def __str__(self):
        return self.name

    def get_template(self, request):
        return "%s/mail/%s.html" % (self._meta.app_label, camelcase_to_underscore(self.__class__.__name__))

    def get_context(self, request, contact):
        return {
            'self': self,
            'contact': contact
        }


class Receipt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now=True)
    success = models.BooleanField(default=False)
