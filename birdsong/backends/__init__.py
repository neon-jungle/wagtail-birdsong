from abc import ABCMeta, abstractmethod

from django.conf import settings


class BaseEmailBackend(metaclass=ABCMeta):
    """
    Abstract class that should be inheritted by all BIRDSONG_BACKENDs.
    """

    @abstractmethod
    def send_campaign(self, request, campaign, contacts, test_send=False):
        """Required be implemented in all backends.
        
        NOTE: Used by Send Campaign action (see `birdsong.options.CampaignAdmin.send_campaign`).
        """
        raise NotImplementedError("You must implement send_campaign() in your BIRDSONG_BACKEND")

    @abstractmethod
    def send_mail(self, subject, template, contact, context):
        """Required to be implemented in all backends.
        
        NOTE: Utilized by Subscribe Form (see `birdsong.views.subscribe`, `birdsong.views.subscribe_api`).
        """
        raise NotImplementedError("You must implement send_mail() in your BIRDSONG_BACKEND")

    @property
    def from_email(self):
        if hasattr(settings, 'BIRDSONG_FROM_EMAIL'):
            return settings.BIRDSONG_FROM_EMAIL
        return settings.DEFAULT_FROM_EMAIL

    @property
    def reply_to(self):
        return getattr(settings, 'BIRDSONG_REPLY_TO', self.from_email)
