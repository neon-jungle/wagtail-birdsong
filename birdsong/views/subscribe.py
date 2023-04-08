from django.conf import settings
from django.utils.translation import gettext as _
from django.db import IntegrityError, transaction
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from wagtail.models import Site

from birdsong.conf import (
    BIRDSONG_BACKEND_CLASS,
    BIRDSONG_ACTIVATION_REQUIRED, BIRDSONG_ACTIVATION_REQUIRED_MSG,
    BIRDSONG_ACTIVATION_EMAIL_SUBJECT,
    BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS, BIRDSONG_SUBSCRIBE_FORM_MSG_FAILURE,
)
from birdsong.forms import SubscribeForm
from birdsong.utils import get_json_http_response, create_contact

DUPLICATE_EMAIL_EXCEPTION = "UNIQUE constraint failed: birdsong_contact.email"
DUPLICATE_KEY_VALUE = "duplicate key value violates unique constraint"

import json

def subscribe(request):
    """Fallback subscription endpoint (alternative to `/subscribe_api`) when JavaScript is disabled/unavailable

    :param request: Request sent to this endpoint
    :type request: class:`requests.models.Request`

    :return: Rendered standalone subscribe form template as an HTTP Response
    :rtype: class:`django.http.HttpResponse`
    """
    if request.method == 'POST': # POST method?
        contact = None
        try:
            form = SubscribeForm(request.POST) # create a form instance and populate it with data from the request
            if form.is_valid(): # is the form valid?
                with transaction.atomic():
                    contact = create_contact(form.cleaned_data['email'])
                    context = {
                        'site_name': settings.WAGTAIL_SITE_NAME,
                        'contact': contact,
                        'activate_url': request.build_absolute_uri(
                            reverse('birdsong:activate', kwargs={'cid': contact.pk, 'token': contact.make_token()})
                        ),
                    }
                    msg = BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS
                    if BIRDSONG_ACTIVATION_REQUIRED:
                        BIRDSONG_BACKEND_CLASS().send_mail(BIRDSONG_ACTIVATION_EMAIL_SUBJECT, 'birdsong/mail/activation_email.html', contact, context)
                        msg += '<br />' + BIRDSONG_ACTIVATION_REQUIRED_MSG if BIRDSONG_ACTIVATION_REQUIRED else ''
                    messages.success(request, msg) # provide at least some feedback when JS is disabled
                    # return HttpResponseRedirect(reverse('birdsong:activation_success')) # NOTE: or alternatively redirect somewhere else?
        except IntegrityError as e: # "Already Subscribed" exception?
            # i.e. django.db.utils.IntegrityError: UNIQUE constraint failed: birdsong_contact.email
            if contact:
                contact.delete()
            if (DUPLICATE_EMAIL_EXCEPTION in str(e) or DUPLICATE_KEY_VALUE in str(e)): # email already subscribed?
                msg = BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS
                if BIRDSONG_ACTIVATION_REQUIRED:
                    msg += '<br />' + BIRDSONG_ACTIVATION_REQUIRED_MSG if BIRDSONG_ACTIVATION_REQUIRED else ''
                messages.success(request, msg) # obfuscate "Already Subscribed" error as success
                form = SubscribeForm()
    else: # GET or any other method?
        form = SubscribeForm() # present a blank form

    return render(
        request, 'birdsong/subscribe.html', context={
            'site': Site.find_for_request(request),
            'form': form,
            'errors': form.errors.as_json(),
        }
    )

def subscribe_api(request):
    """Preferred subscription endpoint (alternative to `/subscribe`) when JavaScript (Ajax) is available

    :param request: Request sent to this endpoint
    :type request: class:`requests.models.Request`

    :return: HTTP Response with JSON body
    :rtype: class:`django.http.HttpResponse`
    """
    if request.method == 'POST':
        contact = None
        try:
            if request.headers.get('Content-Type') == 'application/json': # is json request?
                encoding = request.POST.get("_encoding", 'utf-8')
                body_data = json.loads(request.body.decode(encoding))
                form = SubscribeForm(body_data)
                if form.is_valid():
                    with transaction.atomic():
                        contact = create_contact(form.cleaned_data['email'])
                        context = {
                            'site_name': settings.WAGTAIL_SITE_NAME,
                            'contact': contact,
                            'activate_url': request.build_absolute_uri(
                                reverse('birdsong:activate', kwargs={'cid': contact.pk, 'token': contact.make_token()})
                            ),
                        }
                        msg = BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS
                        if BIRDSONG_ACTIVATION_REQUIRED:
                            BIRDSONG_BACKEND_CLASS().send_mail(BIRDSONG_ACTIVATION_EMAIL_SUBJECT, 'birdsong/mail/activation_email.html', contact, context)
                            msg += '<br />' + BIRDSONG_ACTIVATION_REQUIRED_MSG if BIRDSONG_ACTIVATION_REQUIRED else ''
                        return get_json_http_response(msg)
                else:
                    return get_json_http_response(BIRDSONG_SUBSCRIBE_FORM_MSG_FAILURE, success=False, errors=form.errors.as_json())
        except IntegrityError as e: # "Already Subscribed" exception?
            # i.e. django.db.utils.IntegrityError: UNIQUE constraint failed: birdsong_contact.email
            if contact:
                contact.delete()
            if (DUPLICATE_EMAIL_EXCEPTION in str(e) or DUPLICATE_KEY_VALUE in str(e)): # email already subscribed?
                msg = BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS
                if BIRDSONG_ACTIVATION_REQUIRED:
                    msg += '<br />' + BIRDSONG_ACTIVATION_REQUIRED_MSG if BIRDSONG_ACTIVATION_REQUIRED else ''
                return get_json_http_response(msg) # obfuscate "Already Subscribed" error as success

    return get_json_http_response(_("Bad request"), success=False, status=400) # assume bad request at this point