import json

from django.test import TestCase
from birdsong.utils import html_to_plaintext


class TestUtils(TestCase):

    def test_html_to_plaintext(self):
        # TEST CASES
        test_params = ['html', 'plaintext']
        test_cases = [
            ('<p>Hello World!</p>', 'Hello World!'),
            ("""<!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:600px;" ><![endif]-->
              <div class="mj-column-per-100 mj-outlook-group-fix" style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">
                  <tbody>
                    <tr>
                      <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                        <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;line-height:1;text-align:center;color:#000000;">If you no longer wish to receive these emails click <a href="/newsletter/unsubscribe/3953a0e3-6954-481d-85e2-0b0fe289042a/">here</a> to unsubscribe.</div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>""", 'If you no longer wish to receive these emails click here to unsubscribe.'),
        ]

        # TESTING TEST CASES
        for test_case in test_cases:
            params = {}
            for (i, name) in enumerate(test_params):
                params[name] = test_case[i]
            assert html_to_plaintext(params['html']) == params['plaintext']
