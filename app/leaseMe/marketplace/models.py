from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(User):



class Listing(models.Model):
	address = models.CharField(max_length=50, required=True)
	num_bedrooms = models.IntegerField(required=True)
	num_bathrooms = models.IntegerField(required=True)
	price = models.IntegerField(required=True)
	start_date = models.DateField(required=True)
    end_date = models.DateField(required=True)
    description = models.TextField(max_length=300)
    sold = models.BooleanField(default=False)

