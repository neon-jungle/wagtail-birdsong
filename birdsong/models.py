import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext 
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
        'birdsong.Contact', on_delete=models.CASCADE, related_name='tagged_items')


class Contact(ClusterableModel):
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('email'))
    tags = ClusterTaggableManager(
        through=ContactTag,
        verbose_name=_('tags'),
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    confirmed_at = models.DateTimeField(null=True, verbose_name=_('confirmed at'))
    is_confirmed = models.BooleanField(default=False, verbose_name=_('is confirmed'))

    token = models.UUIDField(default=uuid.uuid4, editable=False)

    panels = [
        FieldPanel('email'),
        FieldPanel('tags'),
    ]

    def __str__(self):
        return self.email


class CampaignStatus(models.IntegerChoices):
    UNSENT = 0, _('unsent')
    SENDING = 1, _('sending')
    SENT = 2, _('sent')
    FAILED = 3, _('failed')


class Campaign(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        help_text=_('The name of the campaign'),
    )
    subject = models.TextField(verbose_name=_('subject'))
    sent_date = models.DateTimeField(
        verbose_name=_('sent date'),
        blank=True,
        null=True,
    )
    receipts = models.ManyToManyField(
        Contact,
        verbose_name=_('receipts'),
        through='Receipt',
    )
    status = models.IntegerField(
        verbose_name=_('status'),
        choices=CampaignStatus.choices,
        default=CampaignStatus.UNSENT
    )

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
    # Probably not necessary, but might come in useful later
    success = models.BooleanField(default=True)


@register_setting
class DoubleOptInSettings(BaseGenericSetting):
    class Meta:
        verbose_name = gettext("Double opt-in settings")

    double_opt_in_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Enable double opt-in"),
        help_text=_(
            "The settings below are only applied if double opt-in is enabled."
        ),
    )

    confirmation_email_subject = models.CharField(
        max_length=150,
        verbose_name=gettext("Subject of confirmation e-mail"),
        default=gettext("Confirm newsletter registration"),
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
        verbose_name=gettext("Content of confirmation e-mail"),
        help_text=gettext(
            "This Text is part of the e-mail that is sent after registration for a campaign"
        ),
        default=gettext(
            "Click the following link if you want register for our newsletter. Otherwise no "
            "action is neccessary."
        ),
    )

    campaign_confirmation_redirect = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=gettext("Redirect page after confirmation of campaign signup"),
    )
    campaign_signup_redirect = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=gettext("Redirect page after signup for a campaign"),
    )
    campaign_unsubscribe_success = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=gettext("Success page for unsubscription"),
    )

    panels = [
        FieldPanel("double_opt_in_enabled"),
        FieldPanel("campaign_signup_redirect"),
        FieldPanel("campaign_confirmation_redirect"),
        FieldPanel("campaign_unsubscribe_success"),
        FieldPanel("confirmation_email_subject"),
        FieldPanel("confirmation_email_body"),
    ]
