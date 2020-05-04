from django.conf.urls import url
from django.urls import reverse
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from birdsong.backends.smtp import SMTPEmailBackend

from .models import Contact
from .views import editor, mail


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, campaign, **kwargs):
        url_helper = AdminURLHelper(self.model)
        sent = bool(campaign.sent_date)

        if not sent:
            buttons = [{
                'url': url_helper.get_action_url('edit', instance_pk=campaign.id),
                'label': 'Edit',
                'classname': 'button button-small bicolor icon icon-cog',
                'title': 'Edit',
            }, {
                'url': url_helper.get_action_url('confirm_send', instance_pk=campaign.id),
                'label': 'Send',
                'classname': 'button button-small button-secondary',
                'title': 'Send',
            }, {
                'url': url_helper.get_action_url('send_test', instance_pk=campaign.id),
                'label': 'Send test',
                'classname': 'button button-small button-secondary',
                'title': 'Send test',
            }, {
                'url': url_helper.get_action_url('view_draft', instance_pk=campaign.id),
                'label': 'View draft',
                'classname': 'button button-small button-secondary',
                'url': url_helper.get_action_url('delete', instance_pk=campaign.id),
                'label': 'Delete',
                'classname': 'button no button-small button-secondary',
                'title': 'Delete',
            }]
        else:
            buttons = [{
                'url': url_helper.get_action_url('inspect', instance_pk=campaign.id),
                'label': 'Inspect',
                'classname': 'button button-small',
                'title': 'Inspect',
            }, {
                'url': url_helper.get_action_url('view_draft', instance_pk=campaign.id),
                'label': 'View sent email',
                'classname': 'button button-small button-secondary',
                'title': 'View sent email',
            }, {
                'url': url_helper.get_action_url('delete', instance_pk=campaign.id),
                'label': 'Delete',
                'classname': 'button no button-small button-secondary',
                'title': 'Delete',
            }]

        return buttons


class CampaignAdmin(ModelAdmin):
    campaign = None
    list_display = ('subject',)
    button_helper_class = EmailCampaignButtonHelper
    inspect_view_enabled = True
    inspect_view_class = editor.InspectCampaign
    inspect_template_name = 'birdsong/editor/inspect_campaign.html'
    backend_class = SMTPEmailBackend
    contact_class = Contact
    contact_filter_class = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        if not self.model and self.campaign:
            self.model = self.campaign
        self.backend = self.backend_class()

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls = (
            url(self.url_helper.get_action_url_pattern('view_draft'), self.view_draft,
                name=self.url_helper.get_action_url_name('view_draft')),
            url(self.url_helper.get_action_url_pattern('confirm_send'), self.confirm_send,
                name=self.url_helper.get_action_url_name('confirm_send')),
            url(self.url_helper.get_action_url_pattern('send_campaign'), self.send_campaign,
                name=self.url_helper.get_action_url_name('send_campaign')),
            url(self.url_helper.get_action_url_pattern('confirm_test'), self.confirm_test,
                name=self.url_helper.get_action_url_name('confirm_test')),
            url(self.url_helper.get_action_url_pattern('send_test'), self.send_test,
                name=self.url_helper.get_action_url_name('send_test')),

        ) + urls

        return urls

    def view_draft(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        contact = self.contact_class.objects.first()
        return editor.view_draft(request, campaign, contact)

    def confirm_send(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        form = self.build_sending_form()
        return editor.confirm_send(
            request,
            campaign,
            form,
            self.url_helper.get_action_url('send_campaign', instance_pk=instance_pk),
            self.url_helper.get_action_url('index')
        )

    def build_sending_form(self):
        if not self.contact_filter_class:
            return None
        contact_filter = self.contact_filter_class()
        return contact_filter.form

    def get_contacts_send_to(self, request):
        if self.contact_filter_class:
            Filter = self.contact_filter_class
            contact_filter = Filter(request.POST)
            return contact_filter.qs
        return self.contact_class.objects.all()

    def send_campaign(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        contacts = self.get_contacts_send_to(request)
        w.tf
        return mail.send_campaign(self.backend, request, campaign, contacts)

    def confirm_test(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        return editor.confirm_test(
            request,
            campaign,
            self.url_helper.get_action_url('send_test', instance_pk),
            self.url_helper.get_action_url('index')
        )

    def send_test(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        if request.method == 'GET':
            return self.confirm_test(request, instance_pk)
        return mail.send_test(self.backend, request, campaign)
