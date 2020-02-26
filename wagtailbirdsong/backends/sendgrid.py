from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings

def send_mail(html):
    message = Mail(
        from_email='from_email@example.com',
        to_emails='jonny@neonjungle.studio',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=html)
    try:
        sg = SendGridAPIClient(settings.SENDGRID_KEY)
        response = sg.send(message)
    except Exception as e:
        print(str(e))