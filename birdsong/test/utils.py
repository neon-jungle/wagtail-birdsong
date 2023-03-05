from birdsong.models import Contact


class BirdsongTestUtils:
    """Various utilities to help with execution of Birdsong Tests"""

    @staticmethod
    def create_test_contact(pk=None, email="bird.song@example.com", is_active=False):
        """Creates and returns an unsaved test Contact instance

        :param pk: Primary Key of the Contact, defaults to None (which means it will be auto-generated)
        :type pk: class:`uuid.UUID`, optional
        :param email: Email of the contact, defaults to "bird.song@example.com"
        :type email: str, optional
        :param is_active: `True` if contact subscription is active, `False` otherwise, defaults to `False`
        :type is_active: bool, optional

        :return: Created Test Contact (unsaved)
        :rtype: class:`bridsong.models.Contact`
        """
        contact = Contact.objects.create()
        if pk:
            contact.pk = pk
        contact.email = email
        contact.is_active = is_active
        return contact

    @staticmethod
    def get_test_contact(pk):
        """Gets the test contact identified by `pk` from DB

        :param pk: Primary Key of the Contact to get (e.g. "162aa314-054b-4219-ba2c-b41124e0691b")
        :type pk: class:`uuid.UUID`

        :return: Contact identified by the `pk`
        :rtype: class:`birdsong.models.Contact`
        """
        return Contact.objects.get(pk=pk)