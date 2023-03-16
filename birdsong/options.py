from django.conf import settings
from django.forms import modelform_factory
from django.http.response import HttpResponseRedirect
from django.urls import re_path
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from wagtail.contrib.modeladmin.helpers import AdminURLHelper, ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin

from birdsong.models import CampaignStatus, Contact, BirdsongSettings
from birdsong.views import actions
from birdsong.views import editor as editor_views

BIRDSONG_DEFAULT_BACKEND = 'birdsong.backends.smtp.SMTPEmailBackend'


class EmailCampaignButtonHelper(ButtonHelper):
    def get_buttons_for_obj(self, campaign, **kwargs):
        url_helper = AdminURLHelper(self.model)

        def button(action_url, label, classnames):
            return {
                'url': url_helper.get_action_url(action_url, instance_pk=campaign.id),
                'label': label,
                'title': label,
                'classname': 'button button-small ' + classnames
            }

        if campaign.status == CampaignStatus.SENDING:
            return [
                button('preview', _('Preview'), 'button-secondary icon icon-view'),
            ]

        sent = campaign.status != CampaignStatus.UNSENT

        delete_btn = button('delete', _('Delete'), 'no button-secondary')
        copy_btn = button('copy', pgettext('Verb', 'Copy'), 'button-secondary')
        if not sent:
            buttons = [
                button('edit', _('Edit'), 'bicolor icon icon-edit'),
                copy_btn,
                button('confirm_send', _('Send'), 'bicolor icon icon-mail'),
                button('send_test', _('Send test'), 'button-secondary icon icon-cog'),
                button('preview', _('Preview'), 'button-secondary icon icon-view'),
                delete_btn,
            ]
        else:
            buttons = [
                button('inspect', _('View'), 'button-secondary icon icon-view'),
                copy_btn,
                delete_btn,
            ]

        return buttons


class CampaignAdmin(ModelAdmin):
    campaign = None
    list_display = ('name', 'status', 'sent_date')
    button_helper_class = EmailCampaignButtonHelper
    inspect_view_enabled = True
    inspect_view_class = editor_views.InspectCampaign
    inspect_template_name = 'birdsong/editor/inspect_campaign.html'
    edit_template_name = 'birdsong/editor/edit_campaign.html'
    edit_view_class = editor_views.EditCampaignView
    create_view_class = editor_views.CreateCampaignView
    create_template_name = 'birdsong/editor/create_campaign.html'
    backend_class = import_string(
        getattr(settings, 'BIRDSONG_BACKEND', BIRDSONG_DEFAULT_BACKEND)
    )

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
            return re_path(
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
            self.url_helper.get_action_url("send_campaign", instance_pk=instance_pk),
            self.url_helper.get_action_url("index"),
        )

    def build_sending_form(self):
        if not self.contact_filter_class:
            return None
        contact_filter = self.contact_filter_class()
        return contact_filter.form

    def get_contacts_send_to(self, request):
        birdsong_settings = BirdsongSettings.load()
        if self.contact_filter_class:
            Filter = self.contact_filter_class
            contact_filter = Filter(request.POST)
            if birdsong_settings.double_opt_in_enabled:
                qs = contact_filter.qs.filter(is_confirmed=True)
            else: 
                qs = contact_filter.qs.filter()
            return qs
        if birdsong_settings.double_opt_in_enabled:
            contacts = self.contact_class.objects.all().filter(is_confirmed=True)
        else: 
            contacts = self.contact_class.objects.all()
        return contacts

    def send_campaign(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        contacts = self.get_contacts_send_to(request)
        return actions.send_campaign(self.backend, request, campaign, contacts)

    def create_contact_form(self, data=None):
        ContactForm = modelform_factory(self.contact_class, exclude=["id"])
        if data:
            return ContactForm(data)
        return ContactForm()

    def confirm_test(self, request, campaign, form):
        return editor_views.confirm_test(
            request,
            campaign,
            form,
            self.url_helper.get_action_url("send_test", campaign.id),
            self.url_helper.get_action_url("index"),
        )

    def send_test(self, request, instance_pk):
        campaign = self.model.objects.get(pk=instance_pk)
        if request.method == "GET":
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
        instance.name = '{} ({})'.format(instance.name, pgettext('noun', 'Copy'))
        instance.pk = None
        instance.id = None
        instance.sent_date = None
        instance.status = CampaignStatus.UNSENT
        instance.save()
        return HttpResponseRedirect(self.url_helper.get_action_url("index"))


class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = "Contacts"
    menu_icon = "user"
    list_display = ("email", "created_at", "confirmed_at", "is_confirmed")
