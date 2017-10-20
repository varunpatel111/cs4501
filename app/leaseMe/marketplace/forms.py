from django import forms

from .models import Listing

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('address', 'num_bedrooms', 'num_bathrooms', 'price', 'start_date', 'end_date', 'description', 'sold', 'user',)