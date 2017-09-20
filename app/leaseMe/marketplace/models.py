from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length=50)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	#just make a simple user for now


class Listing(models.Model):
	address = models.CharField(max_length=50)
	num_bedrooms = models.IntegerField()
	num_bathrooms = models.IntegerField()
	price = models.IntegerField()
	start_date = models.DateField()
	end_date = models.DateField()
	description = models.TextField(max_length=300, blank=True)
	sold = models.BooleanField(default=False)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

