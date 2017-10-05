from django.test import TestCase
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import CustomUser
from .models import Listing
from marketplace import views
import urllib.request
import urllib.parse

class CreateListing(TestCase):
    #setUp method is called before each test in this class
	def setUp(self):
		pass

	@classmethod
	def setUpTestData(self):
		self.c = Client()
		self.resUser = self.c.post('/api/users/create/', {'email': 'dor@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'fried'}).json()
		self.resListSuccess = self.c.post('/api/listings/create/', {'address': '678 Merry Ln.', 'num_bedrooms': 8, 'num_bathrooms': 3, 'price': 290, 'start_date': '2017-06-04', 'end_date': '2017-09-04', 'description': 'Beautiful place on JPA!', 'sold': True, 'user': 1}).json()
		self.resListFailure = self.c.post('/api/listings/create/', {'address': '123 Happy St.', 'num_bedrooms': 4, 'num_bathrooms': 2, 'price': 650, 'start_date': '2017-06-01', 'description': 'Beautiful place on the corner!', 'user': 1}).json()

	def test_success_response(self):
		self.assertEquals(self.resListSuccess['status'], "SUCCESS")

	def test_failure_response(self):
		self.assertEquals(self.resListFailure['status'], "FAILURE")

    #tearDown method is called after each test
	def tearDown(self):
		pass

class GetListing(TestCase):
	def setUp(self):
		pass

	@classmethod
	def setUpTestData(self):
		self.c = Client()
		self.resUser = self.c.post('/api/users/create/', {'email': 'dor@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'fried'}).json()
		self.resListSuccess = self.c.post('/api/listings/create/', {'address': '678 Merry Ln.', 'num_bedrooms': 8, 'num_bathrooms': 3, 'price': 290, 'start_date': '2017-06-04', 'end_date': '2017-09-04', 'description': 'Beautiful place on JPA!', 'sold': True, 'user': 3}).json()
		iD = self.resListSuccess['id']
		string = '/api/listings/' + str(iD) + '/'
		self.response = self.c.get(string)
		self.r = self.response.json()

		iD = 100
		string = '/api/listings/' + str(iD) + '/'
		self.response2 = self.c.get(string)
		self.r2 = self.response2.json()

	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")

	def tearDown(self):
		pass

class DeleteListing(TestCase):
	def setUp(self):
		pass

	@classmethod
	def setUpTestData(self):
		self.c = Client()
		self.resUser = self.c.post('/api/users/create/', {'email': 'dor@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'fried'}).json()
		self.resListSuccess = self.c.post('/api/listings/create/', {'address': '678 Merry Ln.', 'num_bedrooms': 8, 'num_bathrooms': 3, 'price': 290, 'start_date': '2017-06-04', 'end_date': '2017-09-04', 'description': 'Beautiful place on JPA!', 'sold': True, 'user': 2}).json()
		iD = self.resListSuccess['id']
		string = '/api/listings/' + str(iD) + '/'
		self.response = self.c.delete(string)
		self.r = self.response.json()

		iD = 100
		string = '/api/listings/' + str(iD) + '/'
		self.response2 = self.c.delete(string)
		self.r2 = self.response2.json()

	def test_success_response(self):
		self.assertEquals(self.r['status'], "SUCCESS")

	def test_fails_invalid(self):
		self.assertEquals(self.r2['status'], "FAILED")

	def tearDown(self):
		pass
