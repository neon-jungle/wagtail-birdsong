from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from ..models import Contact


def send(request, campaign):
    html = render_to_string(campaign.get_template(request), {'self': campaign, 'request': request})

    contacts = [c.email for c in Contact.objects.all()]

    mail_backend = campaign.get_backend()

    success = mail_backend.send_email(campaign.subject, 'from_email@example.com', contacts, html)

    if success:
        campaign.sent_date = timezone.now()
        campaign.save()
        messages.add_message(request, messages.INFO, f"Campaign with ID {campaign.id} sent")
    else:
        # TODO: Store sent count in BaseEmailBackend.send_email, return and use here if not all succesfully sent
        messages.add_message(request, messages.ERROR, f"Campaign with ID {campaign.id} failed to send")

    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)
