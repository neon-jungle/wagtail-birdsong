from django.db import models
from wagtail.admin.edit_handlers import FieldPanel

class EmailCampaign(models.Model):
    subject = models.TextField()

    panels = [
        FieldPanel('subject'),
    ]

    def get_context(self):
        return {
            "subject": self.subject
        }