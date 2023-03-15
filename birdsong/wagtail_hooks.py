from wagtail.contrib.modeladmin.options import hooks, modeladmin_register, ModelAdmin, ModelAdminGroup

from birdsong.conf import BIRDSONG_ADMIN_GROUP
from birdsong.options import CampaignAdmin
from birdsong.models import Contact, Campaign

@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['icons/birdsong.svg']

class CampaignAdmin(CampaignAdmin):
    campaign = Campaign
    menu_label = 'Campaigns'
    menu_icon = 'mail'
    menu_order = 200

class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Contacts'
    menu_icon = 'user'
    menu_order = 300
    list_diplay = ('email')

def modeladmin_register_birdsong_admin_group(modeladmin_class):
    """Necessary in order to control BirdsongAdminGroup modeladmin registration behaviour"""
    return modeladmin_register(modeladmin_class) if BIRDSONG_ADMIN_GROUP else modeladmin_class

@modeladmin_register_birdsong_admin_group
class BirdsongAdminGroup(ModelAdminGroup):
    menu_item_name = 'birdsong' # needs to be defined at least at this level in order for `modeladmin_re_register` to work properly
    menu_label = 'Birdsong'
    menu_icon = 'birdsong'
    menu_order = 8000 # above wagtail's Reports (9000) menu item
    items = (CampaignAdmin, ContactAdmin)

def modeladmin_re_register(modeladmin_class):
    """Method for re-registering ModelAdmin or ModelAdminGroup classes with Wagtail.

    NOTE: Use it as a decorator in your app's `wagtail_hooks.py` to replace `BirdsongAdminGroup`, for example:
        from birdsong.wagtail_hooks import BirdsongAdminGroup, modeladmin_re_register
        @modeladmin_re_register
        class BirdsongAdminGroup(BirdsongAdminGroup):
            menu_icon = "mail"

    :param modeladmin_class: ModelAdmin class to re-register
    :type modeladmin_class: class:`wagtail.contrib.modeladmin.options.ModelAdminGroup`

    :return: Re-registered ModelAdmin class
    :rtype: class:class:`wagtail.contrib.modeladmin.options.ModelAdminGroup`
    """
    @hooks.register('construct_main_menu')
    def unregister_menu_item(request, menu_items):
        if modeladmin_class.menu_item_name: # modeladmin_class defined or inherited menu_item_name?
            earlierst_item_with_same_name = next((item for item in menu_items if item.name == modeladmin_class.menu_item_name), None) # first match or None
            menu_items[:] = [item for item in menu_items if ((item != earlierst_item_with_same_name))] # filter out earlierst_item_with_same_name
    
    return modeladmin_register(modeladmin_class)
