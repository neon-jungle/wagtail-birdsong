from django.core.mail import send_mass_mail

class BaseEmailBackend:
    def __init__(self, params):
        pass

    def send_email(request, campaign, subject, contacts):
        from_email = campaign.get_from_email()
        messages = ()

        for contact in contacts:
            html = render_to_string(campaign.get_template(request), {'self': campaign, 'request': request, 'contact': contact})
            messages.append((subject, html, from_email, [contact]))

        try:
            send_mass_mail(messages)
            success = True
        except SMTPException as e:
            success = False
            print('There was an error sending an email: ', e) 

        return success

    def unsubscribe_contact(email):
        #TODO: Make this work! And expose an unsubscribe url!
        Contact.objects.get(email=email).delete()
