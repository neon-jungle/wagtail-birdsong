
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from wagtail.models import Site

from birdsong.conf import BIRDSONG_ACTIVATION_TEMPLATE
from birdsong.models import Contact


def activate(request, cidb64, token):
    """Subscription activation endpoint

    :param request: Request sent to this endpoint
    :type request: class:`requests.models.Request`
    :param cidb64: Base64 encoded contact ID (e.g. "YTEwMjA0MzctMGQwYS00ZjBjLWE4MzctMWM2YjgzMDQ3ZjM4")
    :type cidb64: str
    :param token: Subscription Activation Token (e.g. "bkwxpq-cc9a685f0e58c20baacf0ce2c93823f3")
    :type token: str

    :return: Rendered `activate.html` template as an HTTP Response (see `BIRDSONG_ACTIVATION_TEMPLATE`)
    :rtype: class:`django.http.HttpResponse`
    """
    try:
        cid = force_str(urlsafe_base64_decode(cidb64))
        contact = get_object_or_404(Contact, pk=cid) # NOTE: It might be more appropriate to use BIRDSONG_CONTACT_CLASS
    except (TypeError, ValueError, OverflowError, Contact.DoesNotExist):
        raise Http404 # unable to identify contact, let's pretend this endpoint doesn't exist

    if not contact.check_token(token): # token not valid?
        raise Http404() # invalid token, let's pretend this endpoint doesn't exist

    if not contact.is_active: # contact not active yet?
        contact.is_active = True
        contact.save()

    return render(
        request, BIRDSONG_ACTIVATION_TEMPLATE, context={
            'site': Site.find_for_request(request),
            'site_name': settings.WAGTAIL_SITE_NAME,
            'contact': contact,
        }
    )
