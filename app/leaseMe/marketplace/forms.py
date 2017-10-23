from django import forms

from .models import Listing
from .models import CustomUser

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('address', 'num_bedrooms', 'num_bathrooms', 'price', 'start_date', 'end_date', 'description', 'sold')

class UserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

class LoginForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
