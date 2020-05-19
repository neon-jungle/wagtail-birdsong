from django.core.mail import EmailMultiAlternatives, get_connection


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
