from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from birdsong.models import CampaignStatus, Contact, Receipt


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(backend, request, campaign, contacts):
    campaign.status = CampaignStatus.SENDING
    campaign.save()
    backend.send_campaign(request, campaign, contacts)

    return redirect_helper(campaign)


def send_test(backend, request, campaign, test_contact):
    success = backend.send_campaign(
        request, campaign, f"[TEST] {campaign.subject}.", [test_contact])

    if success:
        messages.add_message(request, messages.SUCCESS, f"Test email sent, please check your inbox")
    else:
        messages.add_message(request, messages.ERROR, f"Test email failed to send")

    return redirect_helper(campaign)
