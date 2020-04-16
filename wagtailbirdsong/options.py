from django.urls import reverse
from django.conf.urls import url

from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from .views import editor, mail


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, obj, **kwargs):
        buttons = []

        url_helper = AdminURLHelper(self.model)

        campaign = self.model.objects.get(pk=obj.id)

        if not campaign.sent_date:
            buttons.append({
                'url': url_helper.get_action_url('edit', instance_pk=obj.id),
                'label': 'Edit',
                'classname': 'button button-small bicolor icon icon-cog',
                'title': 'Edit',
            })
            buttons.append({
                'url': url_helper.get_action_url('confirm_send', instance_pk=obj.id),
                'label': 'Send',
                'classname': 'button button-small button-secondary',
                'title': 'Send',
            })
            buttons.append({
                'url': url_helper.get_action_url('view_draft', instance_pk=obj.id),
                'label': 'View draft',
                'classname': 'button button-small button-secondary',
                'title': 'View draft',
            })
            buttons.append({
                'url': url_helper.get_action_url('delete', instance_pk=obj.id),
                'label': 'Delete',
                'classname': 'button no button-small button-secondary',
                'title': 'Delete',
            })
        else:
            buttons.append({
                'url': url_helper.get_action_url('inspect', instance_pk=obj.id),
                'label': 'Inspect',
                'classname': 'button button-small',
                'title': 'Inspect',
            })
            buttons.append({
                'url': url_helper.get_action_url('view_draft', instance_pk=obj.id),
                'label': 'View sent email',
                'classname': 'button button-small button-secondary',
                'title': 'View sent email',
            })

        return buttons



class EmailAdmin(ModelAdmin):
    list_display = ('subject', 'sent_date')
    button_helper_class = EmailCampaignButtonHelper
    inspect_view_enabled = True

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls = (
            url(self.url_helper.get_action_url_pattern('view_draft'), self.view_draft, name=self.url_helper.get_action_url_name('view_draft')), 
            url(self.url_helper.get_action_url_pattern('send'), self.send, name=self.url_helper.get_action_url_name('send')),
            url(self.url_helper.get_action_url_pattern('confirm_send'), self.confirm_send, name=self.url_helper.get_action_url_name('confirm_send')),
        ) + urls

        return urls

    def view_draft(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        return editor.view_draft(request, campaign)

    def send(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        return mail.send(request, campaign)

    def confirm_send(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        return editor.confirm_send(
            request, 
            campaign,
            self.url_helper.get_action_url('send', instance_pk=instance_pk),
            self.url_helper.get_action_url('index')
        )
    
