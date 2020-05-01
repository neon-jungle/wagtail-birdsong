from django.conf import settings

class BaseEmailBackend:
    def send_email(self, request, campaign, subject, contacts):
        raise NotImplementedError

    @property
    def from_email(self):
        if hasattr(settings, 'WAGTAILBIRDSONG_FROM_EMAIL'):
            return settings.WAGTAILBIRDSONG_FROM_EMAIL
        return settings.DEFAULT_FROM_EMAIL