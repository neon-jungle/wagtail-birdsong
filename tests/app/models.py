from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField

from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign, Contact


class SaleCampaign(Campaign):
    body = StreamField(DefaultBlocks())

    panels = Campaign.panels + [
        StreamFieldPanel('body'),
    ]


class ExtendedContact(Contact):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
