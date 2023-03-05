import json

from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from birdsong.test.utils import BirdsongTestUtils


class TestActivateViews(TestCase, BirdsongTestUtils):

    def setUp(self):
        self.test_contact = self.create_test_contact()
        self.test_contact.save()

    def test_activate(self):
        token = self.test_contact.make_token()
        cidb64 = urlsafe_base64_encode(force_bytes(self.test_contact.pk))
        # test garbage activation
        assert self.test_contact.is_active == False # contact should be inactive
        response = self.client.get(reverse('birdsong:activate', kwargs={'cidb64': 'nonsense', 'token': 'nonsense'}))
        assert response.status_code == 404
        response = self.client.get(reverse('birdsong:activate', kwargs={'cidb64': cidb64, 'token': 'nonsense'}))
        assert response.status_code == 404
        self.test_contact = self.get_test_contact(self.test_contact.pk) # refresh test contact after previous garbage activate calls
        assert self.test_contact.is_active == False # contact should be inactive
        # test successful activation
        response = self.client.get(reverse('birdsong:activate', kwargs={'cidb64': cidb64, 'token': token}))
        assert response.status_code == 200 # valid token
        self.test_contact = self.get_test_contact(self.test_contact.pk) # refresh test contact after previous activate call
        assert self.test_contact.is_active == True # contact should now be active
        # test token expiration after activation
        response = self.client.get(reverse('birdsong:activate', kwargs={'cidb64': cidb64, 'token': token}))
        assert response.status_code == 404 # token is no longer vaid after contact activation
        self.test_contact = self.get_test_contact(self.test_contact.pk) # refresh test contact after yet another activate call
        assert self.test_contact.is_active == True # contact should stay active