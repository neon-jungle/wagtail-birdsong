from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from birdsong.options import CampaignAdmin

from .models import ExtendedContact, SaleCampaign, SimpleCampaign


@modeladmin_register
class SaleCampaignAdmin(CampaignAdmin):
    campaign = SaleCampaign
    menu_label = 'Sale Email'
    menu_icon = 'mail'
    menu_order = 200
    contact_class = ExtendedContact



@modeladmin_register
class ContactAdmin(ModelAdmin):
    model = ExtendedContact
    menu_label = 'Contacts'
    menu_icon = 'user'
    list_diplay = ('email', 'first_name', 'last_name', 'location')
