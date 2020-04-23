from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import timezone

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper


def send_helper(request, campaign, subject, contacts):
    mail_backend = campaign.get_backend()

    return mail_backend.send_email(request, campaign, subject, contacts)


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(request, campaign):
    contacts = campaign.get_contact_model().objects.values_list('email', flat=True)
    success = send_helper(request, campaign, campaign.subject, contacts)

    if success:
        campaign.sent_date = timezone.now()
        campaign.save()
        messages.add_message(request, messages.INFO, f"Campaign with ID {campaign.id} sent")
    else:
        messages.add_message(request, messages.ERROR, f"Campaign with ID {campaign.id} failed to send")

    return redirect_helper(campaign)


def send_test(request, campaign):
    test_email = request.POST.get('test_email', False)
    success = send_helper(request, campaign, f"[TEST] {campaign.subject}.", [test_email])

    if success:
        messages.add_message(request, messages.INFO, f"Test email sent, please check your inbox")
    else:
        messages.add_message(request, messages.ERROR, f"Test email failed to send")
    
    return redirect_helper(campaign)

    
