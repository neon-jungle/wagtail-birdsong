import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Site
from wagtail.core.utils import camelcase_to_underscore

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from birdsong.conf import BIRDSONG_ACTIVATION_REQUIRED

class ContactTag(TaggedItemBase):
    content_object = ParentalKey(
        'birdsong.Contact', on_delete=models.CASCADE, related_name='tagged_items')


class Contact(ClusterableModel):

    def get_default_is_active():
        """Determines the default value for `is_active` field based on settings."""
        return not bool(BIRDSONG_ACTIVATION_REQUIRED)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name=_('email'), unique=True)
    tags = ClusterTaggableManager(
        through=ContactTag,
        verbose_name=_('tags'),
        blank=True,
    )
    is_active = models.BooleanField(default=get_default_is_active)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    panels = [
        FieldPanel('email'),
        FieldPanel('tags'),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return self.email

    def make_token(self):
        """Makes token using a `ContactActivationTokenGenerator`.

        :return: Token
        :rtype: str
        """
        return ContactActivationTokenGenerator().make_token(self)
    
    def check_token(self, token):
        """Checks validity of the token.

        :param token: Token to validate e.g. `bkwxds-1d9acfc26be0a0e65b504cab0996718f`
        :type token: str
        :return: `True` if valid, `False` otherwise
        :rtype: bool
        """
        return ContactActivationTokenGenerator().check_token(self, token)

class ContactActivationTokenGenerator(PasswordResetTokenGenerator):
    """Strategy object used to generate and check tokens for the Contact subscription mechanism.

    NOTE: It extends :class:`PasswordResetTokenGenerator` so that it can use its own hash value generator
    """

    def _make_hash_value(self, contact, timestamp):
        """Hash composed out a couple of contact related fields and a timestamp.

        It will be invalidated after contact activation because it utilizes the `is_active` contact field.
        NOTE: Typing `is_active` to boolean first is deliberate so that `None` works the same as `False` or `0`

        :param contact: Client object to generate the token for
        :type contact: class:`birdsong.models.Contact` (see `birdsong.utils.get_contact_model`)
        :param timestamp: Time in seconds to use to make the hash
        :type timestamp: float
        :return: Hash value that will be used during token operations
        :rtype: str
        """
        return str(bool(contact.is_active)) + str(contact.pk) + str(timestamp)

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
