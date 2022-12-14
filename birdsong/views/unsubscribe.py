from django.shortcuts import get_object_or_404, redirect

from birdsong.models import Contact, DoubleOptInSettings


def unsubscribe_user(request, user_id):
    contact = get_object_or_404(Contact, id=user_id)
    contact.delete()

    double_opt_in_settings = DoubleOptInSettings.load(request_or_site=request)

    redirect_url = "/"
    if double_opt_in_settings.campaign_unsubscribe_success:
        redirect_url = double_opt_in_settings.campaign_unsubscribe_success.get_url()

    return redirect(redirect_url)
