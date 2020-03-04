from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from ..backends import sendgrid


def send(request, model, emailcampaign_pk):

    campaign = model.objects.get(pk=emailcampaign_pk)

    html = render_to_string(campaign.get_template(request), {'self': campaign, 'request': request})

    # TODO: Validate it sent correctly
    sendgrid.send_mail(html)

    url_helper = AdminURLHelper(model)
    campaign_list_url = url_helper.get_action_url('index')

    messages.add_message(request, messages.INFO, f"Campaign with ID {emailcampaign_pk} sent")

    return redirect(campaign_list_url)
