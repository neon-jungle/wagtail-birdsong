from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.utils import camelcase_to_underscore

from .blocks import DefaultBlocks


class BaseEmail(models.Model):
    subject = models.TextField()

    # TODO: Make templae path be based on app label etc https://github.com/wagtail/wagtail/blob/master/wagtail/core/models.py#L216
    def get_template(self, request):
        return "%s/mail/%s.html" % (self._meta.app_label, camelcase_to_underscore(self.__class__.__name__))

    class Meta:
        abstract = True


class Contact(models.Model):
    first_name = models.TextField() 
    email = models.EmailField()
