from birdsong.models import Contact, Receipt
from django.http.response import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from wagtail.contrib.modeladmin.views import CreateView, EditView, InspectView


def preview(request, campaign, test_contact):
    return render(request, campaign.get_template(request), campaign.get_context(request, test_contact))


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
    def get_context_data(self, **kwargs):
        context = {
            'receipts': self.instance.receipts.all()
        }
        context.update(kwargs)
        return super().get_context_data(**context)


def ajax_preview(request, view):
    FormClass = view.get_form_class()
    form = FormClass(request.POST)
    if form.is_valid():
        campaign = form.save(commit=False)
        # FIXME won't work with no contacts
        test_contact = Contact.objects.first()
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
