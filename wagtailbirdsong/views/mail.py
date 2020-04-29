from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from wagtail.contrib.modeladmin.helpers.url import AdminURLHelper

from ..models import Receipt, Contact


def send_helper(request, campaign, subject, contacts):
    mail_backend = campaign.get_backend()

    return mail_backend.send_email(request, campaign, subject, contacts)


def redirect_helper(campaign):
    url_helper = AdminURLHelper(type(campaign))
    campaign_list_url = url_helper.get_action_url('index')

    return redirect(campaign_list_url)


def send_campaign(request, campaign):
    contacts = campaign.get_contact_model().objects.all()
    success = send_helper(request, campaign, campaign.subject, contacts)

    if success:
        for contact in contacts:
            Receipt.objects.create(campaign=campaign, contact=contact, sent_date=timezone.now())
        messages.add_message(request, messages.INFO, f"Campaign with ID {campaign.id} sent")
    else:
        messages.add_message(request, messages.ERROR, f"Campaign with ID {campaign.id} failed to send")

    return redirect_helper(campaign)


def send_test(request, campaign):
    test_email = request.POST.get('test_email', False)
    test_contact = Contact.objects.create(email=test_email) # no .save() so don't create a dead contact in the db
    success = send_helper(request, campaign, f"[TEST] {campaign.subject}.", [test_contact])

    if success:
        messages.add_message(request, messages.INFO, f"Test email sent, please check your inbox")
    else:
        messages.add_message(request, messages.ERROR, f"Test email failed to send")
    
    return redirect_helper(campaign)

    
