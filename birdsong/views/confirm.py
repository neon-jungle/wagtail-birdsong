from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from wagtail.core.models import Site

from birdsong.models import BirdsongSettings, Contact


def confirm_contact(request, token):
    contact = get_object_or_404(Contact, token=token)
    contact.is_confirmed = True
    contact.confirmed_at = timezone.now()
    contact.save()

    template = getattr(
        settings,
        'BIRDSONG_CONFIRM_TEMPLATE',
        'confirm.html'
    )
    birdsong_settings = BirdsongSettings.load(request_or_site=request)

    if birdsong_settings.campaign_confirmation_redirect:
        redirect_url = birdsong_settings.campaign_confirmation_redirect.get_url()
        return redirect(redirect_url)
    else:
        site = Site.find_for_request(request)
        return render(
            request, template, context={
                'site': site,
                'contact_email': contact.email,
            }
        )
