from django.conf.urls import url
from django.forms import modelform_factory
from django.urls import reverse
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from birdsong.backends.smtp import SMTPEmailBackend

from .models import Contact
from .views import editor as editor_views
from .views import actions


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, campaign, **kwargs):
        url_helper = AdminURLHelper(self.model)
        sent = bool(campaign.sent_date)

        if not sent:
            buttons = [{
                'url': url_helper.get_action_url('edit', instance_pk=campaign.id),
                'label': 'Edit',
                'classname': 'button button-small bicolor icon icon-edit',
                'title': 'Edit',
            }, {
                'url': url_helper.get_action_url('confirm_send', instance_pk=campaign.id),
                'label': 'Send',
                'classname': 'button button-small bicolor icon icon-mail',
                'title': 'Send',
            }, {
                'url': url_helper.get_action_url('send_test', instance_pk=campaign.id),
                'label': 'Send test',
                'classname': 'button button-small button-secondary icon icon-cog',
                'title': 'Send test',
            }, {
                'url': url_helper.get_action_url('view_draft', instance_pk=campaign.id),
                'label': 'View draft',
                'classname': 'button button-small button-secondary icon icon-view',
                'title': 'View draft',
            }, {
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
    inspect_view_class = editor_views.InspectCampaign
    inspect_template_name = 'birdsong/editor/inspect_campaign.html'
    backend_class = SMTPEmailBackend
    contact_class = Contact
    contact_filter_class = None

    def __init__(self, parent=None):
        if not self.model and self.campaign:
            self.model = self.campaign
        super().__init__(parent=parent)
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
        return editor_views.view_draft(request, campaign, contact)

    def confirm_send(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        form = self.build_sending_form()
        return editor_views.confirm_send(
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
        return actions.send_campaign(self.backend, request, campaign, contacts)

    def create_contact_form(self, data=None):
        ContactForm = modelform_factory(self.contact_class, exclude=['id']) 
        if data:
            return ContactForm(data)
        return ContactForm()

    def confirm_test(self, request, campaign, form):
        return editor_views.confirm_test(
            request,
            campaign,
            form,
            self.url_helper.get_action_url('send_test', campaign.id),
            self.url_helper.get_action_url('index')
        )

    def send_test(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        if request.method == 'GET':
            form = self.create_contact_form()
            return self.confirm_test(request, campaign, form)
        form = self.create_contact_form(request.POST)
        if not form.is_valid():
            return self.confirm_test(request, campaign, form)
        # Create fake contact, send test email
        contact = form.save(commit=False)
        return actions.send_test(self.backend, request, campaign, contact)
