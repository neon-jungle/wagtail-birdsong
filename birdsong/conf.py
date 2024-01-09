from django.conf import settings


BIRDSONG_ADMIN_GROUP = getattr(settings, "BIRDSONG_ADMIN_GROUP", True)

BIRDSONG_TEST_CONTACT = getattr(
    settings, "BIRDSONG_TEST_CONTACT", {"email": "wagtail.birdsong@example.com"}
)
