import logging
from smtplib import SMTPException
from threading import Thread

from django.core.mail import send_mass_mail
from django.db import transaction
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
        try:
            logger.info(f"Sending {len(self.messages)} emails")
            send_mass_html_mail(self.messages)
            logger.info(f"Emails finsihed sending")
            with transaction.atomic():
                c = Campaign.objects.filter(pk=self.campaign_pk).update(
                    status=CampaignStatus.SENT,
                    sent_date=timezone.now(),
                ).first()
                fresh_contacts = Contact.objects.select_for_update().filter(pk__in=self.contact_pks)
                c.receipts.add(*fresh_contacts)
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

        campaign_thread = SendCampaignThread(campaign.pk, [c.pk for c in contacts], messages)
        campaign_thread.start()
