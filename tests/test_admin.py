from time import sleep

from django.core import mail
from django.test import TestCase, TransactionTestCase
from wagtail.core.rich_text import RichText
from wagtail.tests.utils import WagtailTestUtils
from wagtail.tests.utils.form_data import (nested_form_data, rich_text,
                                           streamfield)

from birdsong.models import CampaignStatus
from tests.app.models import ExtendedContact, SaleCampaign


class TestCampaignAdmin(WagtailTestUtils, TestCase):
    def setUp(self):
        self.campaign = SaleCampaign.objects.create(
            name='Test campaign',
            subject='The subject',
            body=[
                ('rich_text', RichText('<p>The body</p>'))
            ]
        )
        self.login()

    def post_data(self, overrides={}):
        post_data = {
            'name': 'Created campaign',
            'subject': 'New subject',
            'body': streamfield([
                ('rich_text', rich_text('<p>Just some content</p>'))
            ])
        }
        post_data.update(overrides)
        return nested_form_data(post_data)

    def test_create(self):
        response = self.client.post(
            '/admin/app/salecampaign/create/', self.post_data(), follow=True
        )
        self.assertEquals(response.status_code, 200)

    def test_edit(self):
        response = self.client.post(
            f'/admin/app/salecampaign/edit/{self.campaign.id}/',
            self.post_data(overrides={'name': 'A Different Name'}),
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'A Different Name')

    def test_preview(self):
        response = self.client.get(
            f'/admin/app/salecampaign/preview/{self.campaign.id}/',
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<p>The body</p>')

    def test_live_preview(self):
        # TODO (post with ajax headers?)
        pass


class TestSending(WagtailTestUtils, TransactionTestCase):
    def setUp(self):
        self.campaign = SaleCampaign.objects.create(
            name='Test campaign',
            subject='The subject',
            body=[
                ('rich_text', RichText('<p>The body</p>'))
            ]
        )
        for person in [
            ('Terry', 'Testington', 'North', 'terry@tests.com', True),
            ('Wag', 'Tail', 'South', 'wag@tail.com', False),
            ('Bird', 'Song', 'North', 'birdsong@example.com', True),
        ]:
            ExtendedContact.objects.create(
                first_name=person[0],
                last_name=person[1],
                location=person[2],
                email=person[3],
                is_active=person[4],
            )
        self.login()

    def test_send_test(self):
        self.client.post(
            f'/admin/app/salecampaign/send_test/{self.campaign.id}/',
            {
                'email': 'have@email.com',
                'first_name': 'Find',
                'last_name': 'Me',
                'location': 'Moon',
            }
        )
        sleep(10)  # Allow time  to send
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue('Hi Find Me' in mail.outbox[0].body)
        self.assertNotEqual(self.campaign.status, CampaignStatus.SENT)

    def test_send(self):
        self.client.get(f'/admin/app/salecampaign/send_campaign/{self.campaign.id}/')

        sleep(10)  # Allow time  to send
        self.assertEquals(len(mail.outbox), 2)
        self.assertEquals(self.campaign.receipts.all().count(), 2)
        # Get fresh from db (altered in a thread)
        fresh_campaign = SaleCampaign.objects.get(pk=self.campaign.pk)
        self.assertEquals(fresh_campaign.status, CampaignStatus.SENT)
