from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)

from .models import Contact


@modeladmin_register
class ContactAdmin(ModelAdmin):
    model = Contact
    menu_label = 'Contacts'
    menu_icon = 'pilcrow'
    menu_order = 200
