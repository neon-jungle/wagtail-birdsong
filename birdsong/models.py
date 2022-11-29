import uuid

from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Site
from wagtail.core.utils import camelcase_to_underscore
from wagtail.contrib.settings.models import (
    register_setting,
    BaseGenericSetting,
)
from wagtail.core.fields import RichTextField


class ContactTag(TaggedItemBase):
    content_object = ParentalKey(
        "birdsong.Contact", on_delete=models.CASCADE, related_name="tagged_items"
    )


class Contact(ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    tags = ClusterTaggableManager(through=ContactTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    panels = [
        FieldPanel("email"),
        FieldPanel("tags"),
    ]

    def __str__(self):
        return self.email


class CampaignStatus(models.IntegerChoices):
    UNSENT = 0
    SENDING = 1
    SENT = 2
    FAILED = 3


class Campaign(models.Model):
    name = models.CharField(max_length=255, help_text="The name of the campaign")
    subject = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)
    receipts = models.ManyToManyField(Contact, through="Receipt")
    status = models.IntegerField(
        choices=CampaignStatus.choices, default=CampaignStatus.UNSENT
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("subject"),
    ]

    def __str__(self):
        return self.name

    def get_template(self, request):
        return "mail/%s.html" % (camelcase_to_underscore(self.__class__.__name__))

    def get_context(self, request, contact):
        site = Site.find_for_request(request)
        return {
            "self": self,
            "contact": contact,
            "site": site,
        }


class Receipt(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now=True)
    # Probably not necessary, but might come in useful later
    success = models.BooleanField(default=True)


@register_setting
class DoubleOptInSettings(BaseGenericSetting):
    class Meta:
        verbose_name = "Double opt-in settings"

    confirmation_email_subject = models.CharField(
        max_length=150,
        verbose_name="Subject of confirmation e-mail",
        default="Confirm newsletter registration",
    )

    confirmation_email_body = RichTextField(
        features=[
            "h2",
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
        ],
        verbose_name="Content of confirmation e-mail",
        help_text="This Text is part of the e-mail that \
            is sent after registration for a campaign.",
        default="Click the following link if you want register \
            for our newsletter. Otherwise no action is neccessary.",
    )

    campaign_confirmation_redirect = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Redirect page after confirmation of campaign signup",
    )
    campaign_signup_redirect = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Redirect page after signup for a campaign",
    )

    panels = [
        FieldPanel("campaign_signup_redirect"),
        FieldPanel("campaign_confirmation_redirect"),
        FieldPanel("confirmation_email_subject"),
        FieldPanel("confirmation_email_body"),
    ]
