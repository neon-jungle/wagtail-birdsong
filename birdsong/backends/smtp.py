import logging
from smtplib import SMTPException
from threading import Thread

from django.db import close_old_connections, transaction
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone

from birdsong.models import Campaign, CampaignStatus, Contact
from birdsong.utils import send_mass_html_mail

from . import BaseEmailBackend

logger = logging.getLogger(__name__)


class SendCampaignThread(Thread):
    def __init__(self, campaign_pk, contact_pks, messages):
        super().__init__()
        self.campaign_pk = campaign_pk
        self.contact_pks = contact_pks
        self.messages = messages

    def run(self):
        campaign = Campaign.objects.get(pk=self.campaign_pk)
        try:
            logger.info(f"Sending {len(self.messages)} emails")
            send_mass_html_mail(self.messages)
            logger.info("Emails finished sending")
            with transaction.atomic():
                campaign.status = CampaignStatus.SENT
                campaign.sent_date = timezone.now()
                campaign.save()
                fresh_contacts = Contact.objects.filter(pk__in=self.contact_pks)
                campaign.receipts.add(*fresh_contacts)
        except SMTPException:
            logger.exception(f"Problem sending campaign: {self.campaign_pk}")
            campaign.status = CampaignStatus.FAILED
            campaign.save()
        finally:
            close_old_connections()


class SMTPEmailBackend(BaseEmailBackend):
    def send_campaign(self, request, campaign, contacts, test_send=False):
        messages = []

        for contact in contacts:
            message_data = {
                'subject': campaign.subject,
                'from_email': self.from_email,
                'to': [contact.email],
                'reply_to': [self.reply_to],

            }
            html_content = render_to_string(
                campaign.get_template(request),
                campaign.get_context(request, contact),
            )
            try:
                text_content = render_to_string(
                    campaign.get_text_template(request),
                    campaign.get_context(request, contact),
                )
                message_data['body'] = text_content
                message_data['html_body'] = html_content
            except TemplateDoesNotExist:
                message_data['body'] = html_content
            messages.append(message_data)
        if test_send:
            # Don't mark as complete, don't worry about threading
            send_mass_html_mail(messages)
        else:
            campaign_thread = SendCampaignThread(
                campaign.pk, [c.pk for c in contacts], messages)
            campaign_thread.start()
