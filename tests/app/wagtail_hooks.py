from birdsong.wagtail_hooks import CampaignAdmin, ContactAdmin, BirdsongAdminGroup, modeladmin_re_register
from .models import SaleCampaign, ExtendedContact

class CampaignAdmin(CampaignAdmin):
    campaign = SaleCampaign
    contact_class = ExtendedContact

class ContactAdmin(ContactAdmin):
    model = ExtendedContact
    list_diplay = ('email', 'first_name', 'last_name', 'location')

@modeladmin_re_register
class BirdsongAdminGroup(BirdsongAdminGroup):
    items = (CampaignAdmin, ContactAdmin)