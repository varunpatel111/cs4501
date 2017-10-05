from django.test import TestCase
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import CustomUser
from .models import Listing
from marketplace import views
import urllib.request
import urllib.parse

class CreateValidListing(TestCase):
	
    #setUp method is called before each test in this class
	def setUp(self):
		self.c = Client()
		self.resUser = self.c.post('/api/users/create/', {'email': 'dor@gmail.com', 'password': 'mynamisv', 'first_name': 'Varun','last_name': 'fried'}).json()
		self.resListSuccess = self.c.post('/api/listings/create/', {'address': '678 Merry Ln.', 'num_bedrooms': 8, 'num_bathrooms': 3, 'price': 290, 'start_date': '2017-06-04', 'end_date': '2017-09-04', 'description': 'Beautiful place on JPA!', 'sold': True, 'user': 1}).json()
		self.resListFailure = self.c.post('/api/listings/create/', {'address': '123 Happy St.', 'num_bedrooms': 4, 'num_bathrooms': 2, 'price': 650, 'start_date': '2017-06-01', 'description': 'Beautiful place on the corner!', 'user': 1}).json()

	def test_success_response(self):
		#response = self.c.post('/api/listings/create/', {'address': '678 Merry Ln.', 'num_bedrooms': 8, 'num_bathrooms': 3, 'price': 290, 'start_date': '2017-06-04', 'end_date': '2017-09-04', 'description': 'Beautiful place on JPA!', 'sold': True, 'user': 1}).json()
		self.assertEquals(self.resListSuccess['status'], "SUCCESS")

	def test_failure_response(self):
		#response = self.c.post('/api/listings/create/', {'address': '123 Happy St.', 'num_bedrooms': 4, 'num_bathrooms': 2, 'price': 650, 'start_date': '2017-06-01', 'description': 'Beautiful place on the corner!', 'user': 1}).json()
		self.assertEquals(self.resListFailure['status'], "FAILURE")

    #tearDown method is called after each test
	def tearDown(self):
		self.resUser = self.c.delete('/api/users/1/').json()
		pass

