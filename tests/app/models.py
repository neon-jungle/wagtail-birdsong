from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign, Contact


class SaleCampaign(Campaign):
    body = StreamField(DefaultBlocks(), use_json_field=True)

    panels = Campaign.panels + [
        FieldPanel('body'),
    ]


class ExtendedContact(Contact):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    panels = Contact.panels + [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('location'),
    ]
