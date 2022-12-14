from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from birdsong.models import Contact, DoubleOptInSettings


def confirm_contact(request, token):
    contact = get_object_or_404(Contact, token=token)
    contact.is_confirmed = True
    contact.confirmed_at = timezone.now()
    contact.save()

    double_opt_in_settings = DoubleOptInSettings.load(request_or_site=request)
    redirect_url = "/"
    if double_opt_in_settings.campaign_confirmation_redirect:
        redirect_url = double_opt_in_settings.campaign_confirmation_redirect.get_url()

    return redirect(redirect_url)
