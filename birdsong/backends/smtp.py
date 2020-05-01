from smtplib import SMTPException

from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from birdsong.utils import send_mass_html_mail

from . import BaseEmailBackend


class SMTPEmailBackend(BaseEmailBackend):
    def send_campaign(self, request, campaign, subject, contacts):
        messages = []

        for contact in contacts:
            content = render_to_string(
                campaign.get_template(request),
                campaign.get_context(request, contact),
            )
            messages.append((subject, content, self.from_email, [contact.email]))

        try:
            send_mass_html_mail(tuple(messages))
            success = True
        except SMTPException as e:
            success = False
            print('There was an error sending an email: ', e)

        return success
