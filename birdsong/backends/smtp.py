import logging
from smtplib import SMTPException
from threading import Thread

from django.db import close_old_connections, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail

from birdsong.utils import send_mass_html_mail
import birdsong.models # NOTE: can't use "from birdsong.models import ..." syntax without risking circular dependency imports in client overloads
                       # NOTE: This is due to BIRDSONG_BACKEND module_loading in birdsong.conf

from . import BaseEmailBackend

logger = logging.getLogger(__name__)


class SendCampaignThread(Thread):
    def __init__(self, campaign_pk, contact_pks, messages):
        super().__init__()
        self.campaign_pk = campaign_pk
        self.contact_pks = contact_pks
        self.messages = messages

    def run(self):
        try:
            logger.info(f"Sending {len(self.messages)} emails")
            send_mass_html_mail(self.messages)
            logger.info("Emails finished sending")
            with transaction.atomic():
                birdsong.models.Campaign.objects.filter(pk=self.campaign_pk).update(
                    status=birdsong.models.CampaignStatus.SENT,
                    sent_date=timezone.now(),
                )
                fresh_contacts = birdsong.models.Contact.objects.filter(
                    pk__in=self.contact_pks)
                birdsong.models.Campaign.objects.get(
                    pk=self.campaign_pk).receipts.add(*fresh_contacts)
        except SMTPException:
            logger.exception(f"Problem sending campaign: {self.campaign_pk}")
            self.campaign.status = birdsong.models.CampaignStatus.FAILED
        finally:
            close_old_connections()


class SMTPEmailBackend(BaseEmailBackend):
    def send_campaign(self, request, campaign, contacts, test_send=False):
        messages = []

        for contact in contacts:
            content = render_to_string(
                campaign.get_template(request),
                campaign.get_context(request, contact),
            )
            messages.append({
                'subject': campaign.subject,
                'body': content,
                'from_email': self.from_email,
                'to': [contact.email],
                'reply_to': [self.reply_to],
            })
        if test_send:
            # Don't mark as complete, don't worry about threading
            send_mass_html_mail(messages)
        else:
            campaign_thread = SendCampaignThread(
                campaign.pk, [c.pk for c in contacts], messages)
            campaign_thread.start()

    def send_mail(self, subject, template, contact, context):
        """Sends out a single email.
        NOTE: This method is here so that birdsong can utilize backends to send subscription activation emails.

        :param subject: Subject of the email
        :type subject: str
        :param template: Template to use for the email (e.g. 'birdsong/mail/activation_email.html')
        :type template: str
        :param contact: Contact to send the email to (see `bridsong.utils.get_contact_model`)
        :type contact: class:`bridsong.models.Contact` or class defined by `BIRDSONG_CONTACT_MODEL` setting
        :param context: Data for the template
        :type context: dict

        :return: 0 on failure, network connection otherwise (see `EmailMessage.send`), 
        :rtype: int|class (defnied by `settings.EMAIL_BACKEND`)
        """
        return send_mail(
            subject,
            render_to_string(template, context),
            self.from_email,
            [contact.email]
        )