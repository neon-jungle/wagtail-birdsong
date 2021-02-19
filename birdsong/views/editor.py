from django.http.response import JsonResponse
from django import shortcuts
from django.template import loader
from wagtail.contrib.modeladmin.views import CreateView, EditView, InspectView

from django.utils.html import escape
from wagtail.core import hooks
from wagtail.core.rich_text.pages import PageLinkHandler 
from wagtail.documents.rich_text import DocumentLinkHandler
from wagtail.core.models import Site
from django.core.exceptions import ObjectDoesNotExist


class PageAbsoluteLinkHandler(PageLinkHandler):
    identifier = "page"
    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            page = cls.get_instance(attrs)
            return f'<a href="{escape(page.full_url)}">'
        except (ObjectDoesNotExist, KeyError):
            return "<a>"

class DocumentAbsoluteLinkHandler(DocumentLinkHandler):
    identifier = "document"
    @classmethod
    def expand_db_attributes(cls, attrs):
        try:
            document = cls.get_instance(attrs)
            root_url = Site.objects.get(is_default_site=True).root_url
            full_url = f"{root_url}{document.url}"
            return f'<a href="{escape(full_url)}">'
        except (ObjectDoesNotExist, KeyError):
            return "<a>"

def register_link_handler(features):
    features.register_link_type(DocumentAbsoluteLinkHandler)
    features.register_link_type(PageAbsoluteLinkHandler)


def render(request, template_name, context, content_type = None, status = None, using = None):
    with hooks.register_temporarily('register_rich_text_features', register_link_handler):
        return shortcuts.render(request, template_name, context, content_type = content_type, status = status, using = using)


def render_to_string(template, context):
    with hooks.register_temporarily('register_rich_text_features', register_link_handler):
       return loader.render_to_string(template, context)

def preview(request, campaign, test_contact):
    return render(
        request,
        campaign.get_template(request),
        campaign.get_context(request, test_contact)
    )


def confirm_send(request, campaign, form, send_url, index_url):
    context = {
        'self': campaign,
        'form': form,
        'request': request,
        'send_url': send_url,
        'index_url': index_url
    }

    return render(request, "birdsong/editor/send_confirm.html", context)


def confirm_test(request, campaign, form, send_url, index_url):
    context = {
        'self': campaign,
        'form': form,
        'request': request,
        'send_url': send_url,
        'index_url': index_url
    }
    return render(request, "birdsong/editor/test_confirm.html", context)


class InspectCampaign(InspectView):
    def __init__(self, model_admin, instance_pk):
        super().__init__(model_admin, instance_pk)
        self.contact_class = model_admin.contact_class

    def get_context_data(self, **kwargs):
        first_receipt = self.instance.receipts.first()
        if first_receipt:
            preview_contact = self.contact_class.objects.filter(
                pk=first_receipt.pk).first()
        else:
            preview_contact = None
        # Should this be frozen? Changes to templates will change old campaigns
        preview = render_to_string(
            self.instance.get_template(self.request),
            self.instance.get_context(self.request, preview_contact),
        )
        context = {
            'receipts': self.instance.receipt_set.all(),
            'preview': preview
        }
        context.update(kwargs)
        return super().get_context_data(**context)


def ajax_preview(request, view):
    FormClass = view.get_form_class()
    form = FormClass(request.POST)
    if form.is_valid():
        campaign = form.save(commit=False)
        contact_class = view.model_admin.contact_class
        # FIXME won't work with no contacts
        test_contact = contact_class.objects.first()
        content = render_to_string(
            campaign.get_template(request),
            campaign.get_context(request, test_contact)
        )
        return JsonResponse({
            'success': True,
            'preview': content,
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class EditCampaignView(EditView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return ajax_preview(request, self)
        return super().post(request, *args, **kwargs)


class CreateCampaignView(CreateView):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return ajax_preview(request, self)
        return super().post(request, *args, **kwargs)
