from django.contrib import messages
from django.shortcuts import redirect
from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from birdsong.models import CampaignStatus


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(backend, request, campaign, contacts):
    campaign.status = CampaignStatus.SENDING
    campaign.save()
    backend.send_campaign(request, campaign, contacts)
    messages.success(request, f"Campaign sent to {len(contacts)} contacts")

    return redirect_helper(campaign)


def send_test(backend, request, campaign, test_contact):
    campaign.subject = f"[TEST] {campaign.subject}"
    backend.send_campaign(request, campaign, [test_contact], test_send=True)
    messages.success(request, "Test email sent, please check your inbox")

    return redirect_helper(campaign)
