from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(models.Model):
	email = models.CharField(max_length=50)
	username = models.CharField(max_length=50, default="")
	password = models.CharField(max_length=50)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)


class Listing(models.Model):
	address = models.CharField(max_length=50)
	num_bedrooms = models.CharField(max_length=50)
	num_bathrooms = models.CharField(max_length=50)
	price = models.CharField(max_length=50)
	start_date = models.CharField(max_length=50)
	end_date = models.CharField(max_length=50)
	description = models.CharField(max_length=300, blank=True)
	sold = models.CharField(max_length=50, default="False")
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Authenticator(models.Model):
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	authenticator = models.CharField(max_length=256)
	date_created = models.CharField(max_length=50)
