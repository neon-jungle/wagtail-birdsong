from django.db import models

try:
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
except ModuleNotFoundError:
    from wagtail.admin.panels import FieldPanel
    from wagtail.admin.panels import FieldPanel as StreamFieldPanel

    # https://docs.wagtail.org/en/stable/releases/3.0.html#removal-of-special-purpose-field-panel-types

try:
    from wagtail.core.fields import StreamField
except ModuleNotFoundError:
    from wagtail.fields import StreamField

from birdsong.blocks import DefaultBlocks
from birdsong.models import Campaign, Contact


class SaleCampaign(Campaign):
    body = StreamField(
        DefaultBlocks(),
        use_json_field=True,
        # added because: django.core.exceptions.ImproperlyConfigured: StreamField must explicitly set use_json_field=True
    )

    panels = Campaign.panels + [
        StreamFieldPanel("body"),
    ]


class ExtendedContact(Contact):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    panels = Contact.panels + [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("location"),
    ]
