from django.shortcuts import render

def view_draft(request, model, emailcampaign_pk):
    campaign = model.objects.get(pk=emailcampaign_pk)
    
    return render(request, campaign.get_template(request), {'self': campaign, 'request': request})