from django.shortcuts import render

def view_draft(request, campaign):
    return render(request, campaign.get_template(request), {'self': campaign, 'request': request})


def confirm_send(request, campaign, send_url, index_url):
    context = {
        'self': campaign, 
        'request': request,
        'send_url': send_url,
        'index_url': index_url
    }

    return render(request, "wagtailbirdsong/editor/send_confirm.html", context)


def confirm_test(request, campaign, send_url, index_url):
    context = {
        'self': campaign, 
        'request': request,
        'send_url': send_url,
        'index_url': index_url
    }

    return render(request, "wagtailbirdsong/editor/test_confirm.html", context)