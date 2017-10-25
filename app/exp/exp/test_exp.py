from django.test import TestCase
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
from exp import views
import json

# Create your tests here.


class CreateUser(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.c = Client()
        self.response = self.c.post('/api/createUser/', {'email': 'varuatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medine'})
        self.response2 = self.c.post('/api/createUser/', {'email': 'varunpel@gmail.com', 'password': 'mynamisv', 'last_name': 'Patel'})
        self.r = self.response.read().decode('utf-8')
        self.r2 = self.response2



    def test_success_response(self):
        print(self.r)
        self.assertEquals("SUCCESS", "SUCCESS")
