import unittest
import requests
from flask import json
from requests.auth import HTTPBasicAuth


basic_url= 'http://localhost:5000/api/v1.0'

class RestfulAPITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_email_pwd_get_posts(self):
        response = requests.get('%s/posts/' % basic_url, auth=HTTPBasicAuth('admin@126.com', '123456'))
        print response.content

    def test_token_get_posts(self):
        token = requests.get('%s/token/' % basic_url, auth=HTTPBasicAuth('admin@126.com', '123456'))
        token_json=json.loads(token.content)
        response = requests.get('%s/posts/' % basic_url, auth=HTTPBasicAuth(token_json['token'], ''))
        print response.content
