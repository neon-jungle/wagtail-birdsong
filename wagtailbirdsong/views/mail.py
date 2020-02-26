from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from ..backends import sendgrid
from ..models import EmailCampaign


def send(request, emailcampaign_pk):
    campaign = EmailCampaign.objects.get(pk=emailcampaign_pk)

    context = campaign.get_context()
    html = render_to_string('wagtailbirdsong/emails/basic-email.html', {})

    # TODO: Validate it sent correctly
    sendgrid.send_mail(html)

    url_helper = AdminURLHelper(EmailCampaign)
    campaign_list_url = url_helper.get_action_url('index')

    messages.add_message(request, messages.INFO, f"Campaign with ID {emailcampaign_pk} sent")

    return redirect(campaign_list_url)
