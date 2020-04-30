from django.core.mail import EmailMultiAlternatives, get_connection


def send_mass_html_mail(datatuple, fail_silently=False, auth_user=None,
                        auth_password=None, connection=None):
    """
    Modified version of send_mass_mail to allow html email
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )

    def _email_from_tuple(tuple):
        msg = EmailMultiAlternatives(*tuple, connection=connection)
        msg.attach_alternative(tuple[1], "text/html")
        return msg

    messages = [_email_from_tuple(m) for m in datatuple]
    return connection.send_messages(messages)
