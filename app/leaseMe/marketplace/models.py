from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(models.Model):
	email = models.CharField(max_length=50, unique=True)
	username = models.CharField(max_length=50, default="", unique=True)
	password = models.CharField(max_length=256)
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

class Recommendation(models.Model):
	listing = models.CharField(unique=True, primary_key=True, default='0', max_length=255)
	listings = models.CharField(max_length=300, default="")
