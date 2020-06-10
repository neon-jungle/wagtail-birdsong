import uuid

from django.conf import settings
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.utils import camelcase_to_underscore
from wagtail.core.models import Site

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from .blocks import DefaultBlocks
from .backends import BaseEmailBackend


class ContactTag(TaggedItemBase):
    content_object = ParentalKey(
        'birdsong.Contact', on_delete=models.CASCADE, related_name='tagged_items')


class Contact(ClusterableModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    tags = ClusterTaggableManager(through=ContactTag, blank=True)

    panels = [
        FieldPanel('email'),
        FieldPanel('tags'),
    ]

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
        return "mail/%s.html" % (camelcase_to_underscore(self.__class__.__name__))

    def get_context(self, request, contact):
        site = Site.find_for_request(request)
        return {
            'self': self,
            'contact': contact,
            'site': site,
        }


class Receipt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now=True)
    success = models.BooleanField(default=False)
