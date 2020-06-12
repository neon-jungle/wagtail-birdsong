from smtplib import SMTPException
from threading import Thread

from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils import timezone

from birdsong.models import CampaignStatus
from birdsong.utils import send_mass_html_mail
import logging
from . import BaseEmailBackend

logger = logging.getLogger(__name__)

class SendCampaignThread(Thread):
    def __init__(self, campaign, messages, contacts):
        super().__init__()
        self.campaign = campaign
        self.messages = messages
        self.contacts = contacts


    def run(self):
        try:
            logger.info(f"Sending {len(self.messages)} emails")
            send_mass_html_mail(self.messages)
            logger.info(f"Emails finsihed sending")
            self.campaign.status = CampaignStatus.SENT
            self.campaign.sent_date = timezone.now()
            self.campaign.create_receipts(self.contacts)
        except SMTPException as e:
            logger.exception(f"Problem sending campaign: {self.campaign}")
            self.campaign.status = CampaignStatus.FAILED
        self.campaign.save()


class SMTPEmailBackend(BaseEmailBackend):
    def send_campaign(self, request, campaign, contacts):
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

        campaign_thread = SendCampaignThread(campaign, messages, contacts)
        campaign_thread.start()
