from django.conf import settings
from django.shortcuts import get_object_or_404, render
from wagtail.core.models import Site

from birdsong.models import Contact


def unsubscribe_user(request, user_id):
    contact = get_object_or_404(Contact, id=user_id)
    contact.delete()

    site = Site.find_for_request(request)

    template = getattr(
        settings,
        'BIRDSONG_UNSUBSCRIBE_TEMPLATE',
        'unsubscribe.html'
    )
    
    return render(
        request, template, context={
            'site': site,
            'contact': contact,
        }
    )

    



    

