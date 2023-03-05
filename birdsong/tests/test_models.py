from django.test import TestCase

from birdsong.test.utils import BirdsongTestUtils
from birdsong.models import ContactActivationTokenGenerator


class TestContactActivationTokenGenerator(TestCase, BirdsongTestUtils):

    def setUp(self):
        self.test_contact = self.create_test_contact()

    def test__make_hash_value(self):
        timestamp = 1678487019.3287854 # test timestamp
        hash_value = ContactActivationTokenGenerator()._make_hash_value(self.test_contact, timestamp)
        assert  hash_value == str(self.test_contact.is_active) + str(self.test_contact.pk) + str(timestamp)
        self.test_contact.is_active = False
        hash_value = ContactActivationTokenGenerator()._make_hash_value(self.test_contact, timestamp)
        assert  hash_value == str(self.test_contact.is_active) + str(self.test_contact.pk) + str(timestamp)


class TestContact(TestCase, BirdsongTestUtils):

    def setUp(self):
        self.test_contact = self.create_test_contact()

    def test_make_check_token(self):
        self.test_contact.is_active = False
        token = self.test_contact.make_token()
        assert self.test_contact.check_token(token) # check token is valid
        self.test_contact.is_active = True # activate contact
        assert not self.test_contact.check_token(token) # check token is invalid after contact activation
        # perform some additional garbage token tests
        assert not self.test_contact.check_token(False)
        assert not self.test_contact.check_token(None)
        assert not self.test_contact.check_token({})
        assert not self.test_contact.check_token('')
        assert not self.test_contact.check_token('nonsense')