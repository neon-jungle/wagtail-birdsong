from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

class BaseEmailBackend:
    def __init__(self, params):
        pass

    def send_email(request, campaign, subject, contacts):
        from_email = campaign.get_from_email()
        messages = []

        for contact in contacts:
            html = render_to_string(campaign.get_template(request), {'self': campaign, 'request': request, 'contact': contact})
            messages.append((subject, html, from_email, [contact.email]))

        try:
            send_mass_mail(tuple(messages))
            success = True
        except SMTPException as e:
            success = False
            print('There was an error sending an email: ', e) 

        return success

    def unsubscribe_contact(campaign_model, email):
        #TODO: Expose an unsubscribe url? Or is that left to the developer...
        campaign_model.objects.get(email=email).delete()
