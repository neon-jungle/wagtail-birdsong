from django.conf.urls import url
from django.forms import modelform_factory
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from birdsong.backends.smtp import SMTPEmailBackend

from .models import Contact
from .views import actions
from .views import editor as editor_views


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, campaign, **kwargs):
        url_helper = AdminURLHelper(self.model)
        sent = bool(campaign.sent_date)

        def button(action_url, label, classnames):
            return {
                'url': url_helper.get_action_url(action_url, instance_pk=campaign.id),
                'label': label,
                'title': label,
                'classname': 'button button-small ' + classnames
            }

        delete_btn = button('delete', 'Delete', 'no button-secondary')
        copy_btn = button('copy', 'Copy', 'button-secondary')
        if not sent:
            buttons = [
                button('edit', 'Edit', 'bicolor icon icon-edit'),
                copy_btn,
                button('confirm_send', 'Send', 'bicolor icon icon-mail'),
                button('send_test', 'Send test', 'button-secondary icon icon-cog'),
                button('preview', 'Preview', 'button-secondary icon icon-view'),
                delete_btn
            ]
        else:
            buttons = [
                button('inspect', 'View', 'button-secondary icon icon-view'),
                copy_btn,
                delete_btn,
            ]

        return buttons


class CampaignAdmin(ModelAdmin):
    campaign = None
    list_display = ('name', 'sent_date')
    button_helper_class = EmailCampaignButtonHelper
    inspect_view_enabled = True
    inspect_view_class = editor_views.InspectCampaign
    inspect_template_name = 'birdsong/editor/inspect_campaign.html'
    edit_template_name = 'birdsong/editor/edit_campaign.html'
    edit_view_class = editor_views.EditCampaignView
    create_view_class = editor_views.CreateCampaignView
    create_template_name = 'birdsong/editor/create_campaign.html'
    backend_class = SMTPEmailBackend
    contact_class = Contact
    contact_filter_class = None
    # FIXME needs to be overwritable
    form_view_extra_js = ['birdsong/js/preview_campaign.js']
    form_view_extra_css = ['birdsong/css/campaign-editor.css']

    def __init__(self, parent=None):
        if not self.model and self.campaign:
            self.model = self.campaign
        super().__init__(parent=parent)
        self.backend = self.backend_class()

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        def gen_url(pattern, view, name=None):
            if not name:
                name = pattern
            return url(
                self.url_helper.get_action_url_pattern(pattern),
                view,
                name=self.url_helper.get_action_url_name(name)
            )
        urls = (
            gen_url('preview', self.preview),
            gen_url('confirm_send', self.confirm_send),
            gen_url('send_campaign', self.send_campaign),
            gen_url('confirm_test', self.confirm_test),
            gen_url('send_test', self.send_test),
            gen_url('copy', self.copy)
        ) + urls

        return urls

    def preview(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        contact = self.contact_class.objects.first()
        return editor_views.preview(request, campaign, contact)


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
    
    def copy(self, request, instance_pk):
        instance = self.model.objects.get(pk=instance_pk)
        instance.name = instance.name + ' (Copy)'
        instance.pk = None
        instance.id = None
        instance.sent_date = None
        instance.save()
        return HttpResponseRedirect(self.url_helper.get_action_url('index'))
