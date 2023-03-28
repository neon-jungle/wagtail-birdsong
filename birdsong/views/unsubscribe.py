from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from wagtail.core.models import Site
from birdsong.models import Contact, BirdsongSettings


def unsubscribe_user(request, user_id):
    contact = get_object_or_404(Contact, id=user_id)
    contact_email = contact.email
    contact.delete()

    template = getattr(
        settings,
        'BIRDSONG_UNSUBSCRIBE_TEMPLATE',
        'unsubscribe.html'
    )
    birdsong_settings = BirdsongSettings.load(request_or_site=request)

    if birdsong_settings.campaign_unsubscribe_success:
        redirect_url = birdsong_settings.campaign_unsubscribe_success.get_url()
        return redirect(redirect_url)
    else:
        site = Site.find_for_request(request)
        return render(
            request, template, context={
                'site': site,
                'contact_email': contact_email,
            }
        )
