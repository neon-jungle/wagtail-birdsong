from birdsong.wagtail_hooks import (BirdsongAdminGroup, CampaignAdmin,
                                    ContactAdmin, modeladmin_re_register)

from .models import ExtendedContact, SaleCampaign


class CampaignAdmin(CampaignAdmin):
    model = SaleCampaign
    contact_class = ExtendedContact


class ContactAdmin(ContactAdmin):
    model = ExtendedContact
    list_display = ("email", "first_name", "last_name", "location")


@modeladmin_re_register
class BirdsongAdminGroup(BirdsongAdminGroup):
    items = (CampaignAdmin, ContactAdmin)
