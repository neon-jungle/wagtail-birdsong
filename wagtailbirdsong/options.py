from django.urls import reverse
from django.conf.urls import url

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from .views import editor, mail


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, **kwargs):
        buttons = super().get_buttons_for_obj(obj, **kwargs)

        url_helper = AdminURLHelper(self.model)

        buttons.append({
            'url': url_helper.get_action_url('send', instance_pk=obj.id),
            'label': 'Send',
            'classname': 'button button-small bicolor icon icon-cog ws-run',
            'title': 'Send',
        })
        buttons.append({
            'url': url_helper.get_action_url('draft', instance_pk=obj.id),
            'label': 'View draft',
            'classname': 'button button-small bicolor icon icon-cog ws-run',
            'title': 'View draft',
        })

        return buttons



class CustomModelAdmin(ModelAdmin):
    button_helper_class = EmailCampaignButtonHelper

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls = (
            url(self.url_helper.get_action_url_pattern('draft'), self.view, name=self.url_helper.get_action_url_name('draft')), 
            url(self.url_helper.get_action_url_pattern('send'), self.send, name=self.url_helper.get_action_url_name('send')),
        ) + urls

        return urls

    def view(self, request, instance_pk):
        return editor.view_draft(request, self.model, instance_pk)

    def send(self, request, instance_pk):
        return mail.send(request, self.model, instance_pk)
    
