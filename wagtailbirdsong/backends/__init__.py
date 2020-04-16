from django.core.mail import send_mail

class BaseEmailBackend:
    def __init__(self, params):
        pass

    def send_email(subject, from_email, contacts, html):
        for contact in contacts:
            # TODO: catch SMTPException and deal with it gracefully
            status = send_mail(
                subject,
                html,
                from_email,
                [contact],
                fail_silently=False,
                html_message=html
            )

        #TODO: Check status' and return a an object of status counts/error
        return True

    def unsubscribe_contact(email):
        Contact.objects.get(email=email).delete()
