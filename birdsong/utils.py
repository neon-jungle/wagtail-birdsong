import re
import json

from django.apps import apps as django_apps
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.html import strip_tags

from birdsong.conf import BIRDSONG_CONTACT_MODEL

def get_contact_model():
    """Returns the Contact model that is active in this project based on `BIRDSONG_CONTACT_MODEL` setting.
    NOTE: Ensure `BIRDSONG_CONTACT_MODEL` is in format of 'app_label.model_name'.

    :raises ImproperlyConfigured: When `BIRDSONG_CONTACT_MODEL` isn't configured properly
    :raises LookupError: When `BIRDSONG_CONTACT_MODEL` can't be discovered
    
    :retrun: Returns a Django model referenced by an app setting `BIRDSONG_CONTACT_MODEL`
    :rtype: class:`birdsong.models.Contact`
    """
    try:
        return django_apps.get_model(BIRDSONG_CONTACT_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "BIRDSONG_CONTACT_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "BIRDSONG_CONTACT_MODEL refers to model '%s' that has not been installed"
            % BIRDSONG_CONTACT_MODEL
        )

def get_json_http_response(message, success = True, errors = None, status = 200):
    """Returns an HTTP Response with a valid JSON formatted body.

    :param message: Message to convey in the response
    :type message: str
    :param success: `True` to convey success, `False` otherwise, defaults to `True`
    :type success: bool, optional
    :param errors: Dictionary of errors, defaults to None
    :type errors: dict, optional
    :param status: HTTP Status Code, defaults to 200
    :type status: int, optional

    :return: HTTP Response with JSON body
    :rtype: class:`django.http.HttpResponse`
    """
    return HttpResponse(
        content=json.dumps({
            "success": success,
            "message": message,
            "errors": errors,

        }),
        status=status
    )
    
def create_contact(email):
    """Creates a new contact with email and returns it back.
    NOTE: Utilizes `bridsong.utils.get_contact_model` method which honors `BIRDSONG_CONTACT_MODEL` setting.

    :param email: Email of the new contact record.
    :type email: str

    :return: Newly created contact record
    :rtype: class:`bridsong.models.Contact` or class defined by `BIRDSONG_CONTACT_MODEL` setting
    """
    contact = get_contact_model()()
    # contact.is_valid = contact.get_default_is_active()
    contact.email = email
    contact.save() # NOTE: Relies on UNIQUE email constraint to prevent duplicates
    return contact

def html_to_plaintext(html):
    """
    Converts `html` to plaintext.

    :param html: HTML formatted string
    :type html: str

    :return: Plaintext representation of the HTML input
    :rtype: str
    """
    plaintext = re.sub('[ \t]+', ' ', strip_tags(html)) # Remove html tags and continuous whitespaces 
    plaintext = plaintext.replace('\n ', '\n').strip() # Strip single spaces in the beginning of each line
    return plaintext

def send_mass_html_mail(email_data, fail_silently=False, auth_user=None,
                        auth_password=None, connection=None):
    """
    Modified version of send_mass_mail to allow html email
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )

    def _email_from_dict(data):
        msg = EmailMultiAlternatives(connection=connection, **data)
        msg.attach_alternative(data['body'], "text/html")
        return msg

    messages = [_email_from_dict(d) for d in email_data]
    return connection.send_messages(messages)
