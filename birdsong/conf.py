from django.conf import settings
import django.utils.module_loading as module_loading
from django.utils.translation import gettext as _

### BIRDSONG_CONTACT ###
BIRDSONG_CONTACT_MODEL = getattr(settings, 'BIRDSONG_CONTACT_MODEL', 'birdsong.Contact')

### BIRDSONG_TEST_CONTACT ###
BIRDSONG_TEST_CONTACT = getattr(settings, 'BIRDSONG_TEST_CONTACT', { 'email': 'wagtail.birdsong@example.com' })

### BIRDSONG_ADMIN ###
BIRDSONG_ADMIN_GROUP = getattr(settings, 'BIRDSONG_ADMIN_GROUP', True)

### BIRDSONG_BACKEND ###
BIRDSONG_BACKEND = getattr(settings, 'BIRDSONG_BACKEND', 'birdsong.backends.smtp.SMTPEmailBackend')
BIRDSONG_BACKEND_CLASS = module_loading.import_string(BIRDSONG_BACKEND)

### BIRDSONG_SUBSCRIBE_FORM ###
BIRDSONG_SUBSCRIBE_FORM_AJAX = getattr(settings, 'BIRDSONG_SUBSCRIBE_FORM_AJAX', True) # post form with ajax
BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS = _(getattr(settings, 'BIRDSONG_SUBSCRIBE_FORM_MSG_SUCCESS', 'You have been subscribed.')) # presented upon valid form submission
BIRDSONG_SUBSCRIBE_FORM_MSG_FAILURE = _(getattr(settings, 'BIRDSONG_SUBSCRIBE_FORM_MSG_FAILURE', 'Invalid email address')) # presented upon invalid form submission

### BIRDSONG_ACTIVATION ###
BIRDSONG_ACTIVATION_REQUIRED = getattr(settings, 'BIRDSONG_ACTIVATION_REQUIRED', False)
BIRDSONG_ACTIVATION_REQUIRED_MSG = _(getattr(settings, 'BIRDSONG_ACTIVATION_REQUIRED_MSG', 'Check your e-mail to activate your subscription.'))
BIRDSONG_ACTIVATION_EMAIL_SUBJECT = _(getattr(settings, 'BIRDSONG_ACTIVATION_EMAIL_SUBJECT', 'Activate Your ' +
    getattr(settings, 'WAGTAIL_SITE_NAME', '') + ' Mailing List Subscription'))

