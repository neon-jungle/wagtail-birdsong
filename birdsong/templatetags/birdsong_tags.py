from django import template

from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _

from wagtail.models import Site

from birdsong.forms import SubscribeForm

from birdsong.conf import (
    BIRDSONG_SUBSCRIBE_FORM_ID, BIRDSONG_SUBSCRIBE_FORM_BUTTON_LABEL, BIRDSONG_SUBSCRIBE_FORM_AJAX,
    BIRDSONG_SUBSCRIBE_FORM_NOVALIDATE, BIRDSONG_SUBSCRIBE_FORM_FEEDBACK
)

register = template.Library()

@register.inclusion_tag("birdsong/tags/subscribe.html", takes_context=True)
def birdsong_subscribe_form(context):
    """Renders the Subscribe form template tag.
    NOTE: Aimed to be used in client apps' templates. (see `birdsong/templates/birdsong/subscribe.html`)

    :param context: Data for the template
    :type context: dict

    :return: Data for the rendered template tag
    :rtype: dict
    """
    if context.request.method == 'POST': # POST method?
        form = SubscribeForm(context.request.POST) # create a subscribe form and populate it with posted data
    else: # GET or any other method?
        form = SubscribeForm() # create a blank subscribe form

    return { 
        "messages": messages.get_messages(context.request),
        "site": Site.find_for_request(context.request),
        "request": context.request,
        "form_action": reverse('birdsong:subscribe'),
        "subscribe_api_url": reverse('birdsong:subscribe_api'),
        "form": form,
        "errors": form.errors.as_json(),
        "BIRDSONG_SUBSCRIBE_FORM_ID": BIRDSONG_SUBSCRIBE_FORM_ID,
        "BIRDSONG_SUBSCRIBE_FORM_BUTTON_LABEL": BIRDSONG_SUBSCRIBE_FORM_BUTTON_LABEL,
        "BIRDSONG_SUBSCRIBE_FORM_AJAX": BIRDSONG_SUBSCRIBE_FORM_AJAX,
        "BIRDSONG_SUBSCRIBE_FORM_NOVALIDATE": BIRDSONG_SUBSCRIBE_FORM_NOVALIDATE,
        "BIRDSONG_SUBSCRIBE_FORM_FEEDBACK": BIRDSONG_SUBSCRIBE_FORM_FEEDBACK,
        "FORM_EXPIRED_ERROR": _("Form expired (try to refresh the page)"),
        "FORM_UNEXPECTED_ERROR": _("Internal Server Error (try again later)"),
    }