from django.conf.urls import include, url
from django.urls import reverse

from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from wagtail.core import hooks

from . import urls
from .models import EmailCampaign


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^wagtailbirdsong/emailcampaign/', include(urls), name='list_campaigns'),
    ]


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, **kwargs):
        buttons = super().get_buttons_for_obj(obj, **kwargs)
        buttons.append({
            'url': reverse('wagtailbirdsong:send', kwargs={'emailcampaign_pk': obj.id}),
            'label': 'Send',
            'classname': 'button button-small bicolor icon icon-cog ws-run',
            'title': 'Send',
        })

        return buttons


class EmailCampaignAdmin(ModelAdmin):
    model = EmailCampaign
    button_helper_class = EmailCampaignButtonHelper
    menu_label = 'Campaign'
    menu_icon = 'pilcrow'
    menu_order = 200

modeladmin_register(EmailCampaignAdmin)