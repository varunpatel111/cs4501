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
        self.response = self.c.post('/api/createUser/', {'email': 'dfjk@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'d34'})
        self.r = self.response.json()

    def test_success_response(self):
        print(self.r)
        self.assertEquals(self.r['status'], "SUCCESS")

    def tearDown(self):
        pass


class CreateBadUser(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.c = Client()
        self.response = self.c.post('/api/createUser/', {'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'d34'})
        self.r = self.response.json()

    def test_success_response(self):
        print(self.r)
        self.assertEquals(self.r['status'], "FAILED")

    def tearDown(self):
        pass

class LoginBadUser(TestCase):
    #setUp method is called before each test in this class
    def setUp(self):
        self.c = Client()
        self.response = self.c.post('/api/userLogin/', {'username':'d3sdf4', 'password' : "sdlfjskdf"})
        self.r = self.response.json()

    def test_success_response(self):
        print(self.r)
        self.assertEquals(self.r['status'], "FAILED")

    def tearDown(self):
        pass
