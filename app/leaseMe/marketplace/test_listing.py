from django.test import TestCase
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import CustomUser
from .models import Listing
from marketplace import views
import urllib.request
import urllib.parse
# Create your tests here.


class CreateListing(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.response = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel'})
		self.response2 = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'last_name': 'Patel'})
		self.r = self.response.json()
		self.r2 = self.response2.json()
	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

    #user_id not given in url, so error
	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")
		self.assertEquals(self.response2.status_code, 400)

    #tearDown method is called after each test
	def tearDown(self):
		pass

class GetListing(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.response = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel'})
		iD = self.response.json()['id']
		string = '/api/users/' + str(iD) + '/'
		self.response = self.c.get(string)
		self.r = self.response.json()

		self.response2 = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel'})
		iD = int(self.response2.json()['id']) + 100
		string = '/api/users/' + str(iD) + '/'
		self.response2 = self.c.get(string)
		self.r2 = self.response2.json()

	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

    #user_id not given in url, so error
	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")

    #tearDown method is called after each test
	def tearDown(self):
		pass
