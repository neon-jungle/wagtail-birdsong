from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from birdsong.models import Receipt, Contact


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(backend, request, campaign, contacts):
    success = backend.send_campaign(
        request, campaign, campaign.subject, contacts)

    if success:
        for c in contacts:
            try:
                # We do this in case a Contact has been deleted after a campaign has been sent - it's happened :(
                contact = Contact.objects.get(id=c.id)
                Receipt.objects.create(
                    contact=contact,
                    campaign=campaign,
                    success=True
                )
            except Contact.DoesNotExist:
                continue
        campaign.sent_date = timezone.now()
        campaign.save()
        messages.add_message(
            request, messages.SUCCESS, f"Campaign '{campaign.name}' sent to {len(contacts)} contacts")
    else:
        messages.add_message(request, messages.ERROR,
                             f"Campaign '{campaign.name}' failed to send")

    return redirect_helper(campaign)


def send_test(backend, request, campaign, test_contact):
    success = backend.send_campaign(
        request, campaign, f"[TEST] {campaign.subject}.", [test_contact])

    if success:
        messages.add_message(request, messages.SUCCESS, f"Test email sent, please check your inbox")
    else:
        messages.add_message(request, messages.ERROR, f"Test email failed to send")

    return redirect_helper(campaign)
