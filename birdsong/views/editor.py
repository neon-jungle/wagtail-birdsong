from django.shortcuts import render
from wagtail.contrib.modeladmin.views import IndexView, InspectView

from ..models import Receipt

def view_draft(request, campaign, test_contact):
    return render(request, campaign.get_template(request), campaign.get_context(request, test_contact))


def confirm_send(request, campaign, send_url, index_url):
    context = {
        'self': campaign, 
        'request': request,
        'send_url': send_url,
        'index_url': index_url
    }

    return render(request, "birdsong/editor/send_confirm.html", context)


def confirm_test(request, campaign, send_url, index_url):
    context = {
        'self': campaign, 
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