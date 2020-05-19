from django.conf import settings

class BaseEmailBackend:
    def send_email(self, request, campaign, subject, contacts):
        raise NotImplementedError

    @property
    def from_email(self):
        if hasattr(settings, 'BIRDSONG_FROM_EMAIL'):
            return settings.BIRDSONG_FROM_EMAIL
        return settings.DEFAULT_FROM_EMAIL

    @property
    def reply_to(self):
        return getattr(settings, 'BIRDSONG_REPLY_TO', self.from_email)