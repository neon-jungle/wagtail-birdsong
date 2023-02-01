from django.conf import settings

BIRDSONG_TEST_CONTACT = getattr(settings, 'BIRDSONG_TEST_CONTACT', { 'email': 'wagtail.birdsong@example.com' })