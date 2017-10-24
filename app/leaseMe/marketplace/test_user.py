from django.test import TestCase
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import CustomUser
from .models import Listing
from marketplace import viewsAuthenticator
from marketplace import viewsListings
from marketplace import viewsUsers
import urllib.request
import urllib.parse
# Create your tests here.


class CreateUser(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.response = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medicine'})
		self.response2 = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'last_name': 'Patel'})
		self.r = self.response.json()
		self.r2 = self.response2.json()
	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

    #user_id not given in url, so error
	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")

    #tearDown method is called after each test
	def tearDown(self):
		pass

class GetUser(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.response = self.c.post('/api/users/create/', {'email': 'varunpatsdfel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medsdficine'})
		iD = self.response.json()['id']
		string = '/api/users/' + str(iD) + '/'
		self.response = self.c.get(string)
		self.r = self.response.json()

		self.response2 = self.c.post('/api/users/create/', {'email': 'vsdf@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medisacine'})
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

class DeleteUser(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.response = self.c.post('/api/users/create/', {'email': 'varunpatel@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medifffcine'})
		iD = self.response.json()['id']
		string = '/api/users/' + str(iD) + '/'
		self.response = self.c.delete(string)
		self.r = self.response.json()

		self.response2 = self.c.post('/api/users/create/', {'email': 'v@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'Patel', 'username':'medfficine'})
		iD = int(self.response2.json()['id']) + 100
		string = '/api/users/' + str(iD) + '/'
		self.response2 = self.c.delete(string)
		self.r2 = self.response2.json()

	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

    #user_id not given in url, so error
	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")

    #tearDown method is called after each test
	def tearDown(self):
		pass
