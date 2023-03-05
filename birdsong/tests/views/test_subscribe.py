import json

from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse

CONTENT_TYPE_JSON = 'application/json'


class TestSubscribeViews(TestCase):

    def test_subscribe(self):
        url = reverse('birdsong:subscribe')

        ERRORS_EMAIL_FIELD_REQUIRED = '{"email": [{"message": "This field is required.", "code": "required"}]}'
        ERRORS_EMAIL_FIELD_INVALID = '{"email": [{"message": "Enter a valid email address.", "code": "invalid"}]}'

        # TEST CASES
        test_params = ['method', 'content_type', 'data', 'expected_status_code', 'expected_errors']
        test_cases = [
            ('GET', None, None, 200, '{}'), # GET requests should return back an empty form
            ('GET', MULTIPART_CONTENT, {'nonsense': 'nonsense'}, 200, '{}'),  # GET requests should return back an empty form
            ('POST', MULTIPART_CONTENT, None, 200, ERRORS_EMAIL_FIELD_REQUIRED), # email is required
            ('POST', MULTIPART_CONTENT, {}, 200, ERRORS_EMAIL_FIELD_REQUIRED), # email is required
            ('POST', MULTIPART_CONTENT, {'nonsense': 'nonsense'}, 200, ERRORS_EMAIL_FIELD_REQUIRED), # email is required
            ('POST', MULTIPART_CONTENT, {'email': ''}, 200, ERRORS_EMAIL_FIELD_REQUIRED), # email is required
            ('POST', MULTIPART_CONTENT, {'email': ''}, 200, ERRORS_EMAIL_FIELD_REQUIRED), # email is required
            ('POST', MULTIPART_CONTENT, {'email': 'nonsense'}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': 'bad@data'}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<IMG SRC="jav ascript:alert('XSS');">'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<IMG SRC="jav&#x09;ascript:alert('XSS');">'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<<SCRIPT>alert("XSS");//\<</SCRIPT>'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<IMG SRC="('XSS')"'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''Set.constructor`alert\x28document.domain\x29'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<BODY ONLOAD=alert('XSS')>'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', MULTIPART_CONTENT, {'email': '''<svg/onload=alert('XSS')>'''}, 200, ERRORS_EMAIL_FIELD_INVALID), # email is invalid
            ('POST', CONTENT_TYPE_JSON, {'email': 'bird.song@example.com'}, 200, ERRORS_EMAIL_FIELD_REQUIRED), # this endpoint doesn't understand json
            ('POST', MULTIPART_CONTENT, {'email': 'bird.song@example.com'}, 200, '{}'), # success
            ('POST', MULTIPART_CONTENT, {'email': 'bird.song@example.com'}, 200, '{}'), # pretended success (ignoring duplicate email)
        ]

        # TESTING TEST CASES
        for test_case in test_cases:
            params = {}
            for (i, name) in enumerate(test_params):
                params[name] = test_case[i]
            if params['method'] == 'GET':
                response = self.client.get(url, data=params['data'], content_type=params['content_type'])
            else:
                response = self.client.post(url, data=params['data'], content_type=params['content_type'])
            assert response.status_code == params['expected_status_code']
            assert response.context.get('errors') == params['expected_errors']

    def test_subscribe_api(self):
        url = reverse('birdsong:subscribe_api')

        # TEST CASES
        test_params = ['method', 'content_type', 'data', 'expected_status_code', 'success', 'expect_errors']
        test_cases = [
            ('GET', None, None, 400, None, None), # wrong method
            ('GET', CONTENT_TYPE_JSON, {'email': 'birdsong@example.com'}, 400, False, True), # wrong method
            ('GET', None, {'email': 'bird.song@example.com'}, 400, False, True), # wrong method & bad content type
            ('POST', MULTIPART_CONTENT, {'email': 'bird.song@example.com'}, 400, None, None), # bad content type
            ('POST', CONTENT_TYPE_JSON, {'nonsense': 'nonsense'}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': 'bad.data'}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': 'bad@data'}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': 'bad@data@data'}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<IMG SRC="jav ascript:alert('XSS');">'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<IMG SRC="jav&#x09;ascript:alert('XSS');">'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<<SCRIPT>alert("XSS");//\<</SCRIPT>'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<IMG SRC="('XSS')"'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''Set.constructor`alert\x28document.domain\x29'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<BODY ONLOAD=alert('XSS')>'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': '''<svg/onload=alert('XSS')>'''}, 200, False, True), # bad data
            ('POST', CONTENT_TYPE_JSON, {'email': 'bird.song@example.com'}, 200, True, False), # success
            ('POST', CONTENT_TYPE_JSON, {'email': 'bird.song@example.com'}, 200, True, False), # pretended success (ignoring duplicate email)
        ]

        # TESTING TEST CASES
        for test_case in test_cases:
            params = {}
            for (i, name) in enumerate(test_params):
                params[name] = test_case[i]
            if params['method'] == 'GET':
                response = self.client.get(url, data=params['data'], content_type=params['content_type'])
            else:
                response = self.client.post(url, data=params['data'], content_type=params['content_type'])
            assert response.status_code == params['expected_status_code']
            if response.status_code == 200:
                json_response = json.loads(response.content.decode())
                assert json_response['success'] == params['success']
                assert bool(json_response['errors']) == params['expect_errors']