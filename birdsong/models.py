import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.coreutils import camelcase_to_underscore
from wagtail.models import Site


class ContactTag(TaggedItemBase):
    content_object = ParentalKey(
        "birdsong.Contact", on_delete=models.CASCADE, related_name="tagged_items"
    )


class Contact(ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_("email"))
    tags = ClusterTaggableManager(
        through=ContactTag,
        verbose_name=_("tags"),
        blank=True,
    )

    panels = [
        FieldPanel("email"),
        FieldPanel("tags"),
    ]

    def __str__(self):
        return self.email


class CampaignStatus(models.IntegerChoices):
    UNSENT = 0, _("unsent")
    SENDING = 1, _("sending")
    SENT = 2, _("sent")
    FAILED = 3, _("failed")


class Campaign(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        help_text=_("The name of the campaign"),
    )
    subject = models.TextField(verbose_name=_("subject"))
    sent_date = models.DateTimeField(
        verbose_name=_("sent date"),
        blank=True,
        null=True,
    )
    receipts = models.ManyToManyField(
        Contact,
        verbose_name=_("receipts"),
        through="Receipt",
    )
    status = models.IntegerField(
        verbose_name=_("status"),
        choices=CampaignStatus.choices,
        default=CampaignStatus.UNSENT,
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
