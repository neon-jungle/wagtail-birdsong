import json

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings

sg = SendGridAPIClient(settings.SENDGRID_KEY)

def send_mail(html):
    message = Mail(
        from_email='from_email@example.com',
        to_emails='jonny@neonjungle.studio',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=html)
    try:
        response = sg.send(message)
    except Exception as e:
        #TODO: Proper error handling
        print(str(e))


def subscribe_user(user):
    try:
        sg.client.marketing.contacts.put(
            request_body=dict(
                list_ids=[settings.SENDGRID_LIST_ID], 
                contacts=[{'email': user.email, 'first_name': user.first_name}]
            )
        )
    except Exception as e:
        #TODO: Proper error handling
        print(str(e))


def unsubscribe_user(user):
    try:
        response = sg.client.marketing.contacts.search.post(
            request_body=dict(
                query=f"email LIKE '{user.email}%' AND CONTAINS(list_ids, '{settings.SENDGRID_LIST_ID}')"
            )
        )

        response = json.loads(response.body)

        if response.get('contact_count') > 0:
            ids = [u.get('id') for u in response.get('result')]
            res = sg.client.marketing.contacts.delete(
                query_params={'ids': ','.join(ids)}
            )

    except Exception as e:
        #TODO: Proper error handling
        print(str(e))
        