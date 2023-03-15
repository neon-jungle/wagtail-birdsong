from django.conf import settings
import django.utils.module_loading as module_loading
from django.utils.translation import gettext as _

### BIRDSONG_ADMIN ###
BIRDSONG_ADMIN_GROUP = getattr(settings, 'BIRDSONG_ADMIN_GROUP', True)

### BIRDSONG_CONTACT ###
BIRDSONG_CONTACT_MODEL = getattr(settings, 'BIRDSONG_CONTACT_MODEL', 'birdsong.Contact')

### BIRDSONG_TEST_CONTACT ###
BIRDSONG_TEST_CONTACT = getattr(settings, 'BIRDSONG_TEST_CONTACT', { 'email': 'wagtail.birdsong@example.com' })

