from django.shortcuts import render

from ..models import EmailCampaign

def view_draft(request, emailcampaign_pk):
    campaign = EmailCampaign.objects.get(pk=emailcampaign_pk)

    context = campaign.get_context()
    
    return render(request, 'wagtailbirdsong/emails/basic-email.html', context)