from django.test import TestCase
from wagtail.core.rich_text import RichText
from wagtail.tests.utils import WagtailTestUtils
from wagtail.tests.utils.form_data import (nested_form_data, rich_text,
                                           streamfield)

from tests.app.models import SaleCampaign


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
        self.assertContains(response, '<p>Just some content</p>')


    def test_live_preview(self):


class TestSending(WagtailTestUtils, TestCase):
    def setUp(self):
        self.campaign = SaleCampaign.objects.create(
            name='Test campaign',
            subject='The subject',
            body=[
                ('rich_text', RichText('<p>The body</p>'))
            ]
        )
        for email in [
            ''
        ]
        self.login()

    def test_send_test(self):
        

    def test_send(self):
        pass

