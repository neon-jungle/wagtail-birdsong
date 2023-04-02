import json

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch

from birdsong.test.utils import BirdsongTestUtils


class TestActivateViews(TestCase, BirdsongTestUtils):

    def setUp(self):
        self.test_contact = self.create_test_contact()
        self.test_contact.save()

    def test_activate(self):
        token = self.test_contact.make_token()
        cid = self.test_contact.pk

        assert self.test_contact.is_active == False # contact should be inactive at first

        # test garbage activations
        with self.assertRaises(NoReverseMatch): # invalid cid and invalid token
            response = self.client.get(reverse('birdsong:activate', kwargs={'cid': 'nonsense', 'token': 'nonsense'}))
        with self.assertRaises(NoReverseMatch): # invalid cid but valid token
            response = self.client.get(reverse('birdsong:activate', kwargs={'cid': 'nonsense', 'token': token}))
        response = self.client.get(reverse('birdsong:activate', kwargs={'cid': cid, 'token': 'nonsense'})) # valid cid but invalid token
        assert response.status_code == 404
        self.test_contact = self.get_test_contact(cid) # refresh test contact
        assert self.test_contact.is_active == False # contact should still be inactive

        # test successful activation
        response = self.client.get(reverse('birdsong:activate', kwargs={'cid': cid, 'token': token}))
        assert response.status_code == 200 # valid token
        self.test_contact = self.get_test_contact(cid) # refresh test contact
        assert self.test_contact.is_active == True # contact should now be active

        # test token expiration after activation
        response = self.client.get(reverse('birdsong:activate', kwargs={'cid': cid, 'token': token}))
        assert response.status_code == 404 # token is no longer vaid after contact activation
        self.test_contact = self.get_test_contact(cid) # refresh test contact
        assert self.test_contact.is_active == True # contact should stay active