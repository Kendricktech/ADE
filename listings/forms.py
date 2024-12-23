from django.forms import ModelForm, modelformset_factory
from django import forms
from django.core.exceptions import ValidationError
from .models import Listing, SubImage

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'price',
            'num_bedrooms',
            'num_bathrooms',
            'square_footage',
            'address',
            'main_image',  # Main image for the listing
        ]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be a positive number.")
        return price

    def clean_num_bedrooms(self):
        num_bedrooms = self.cleaned_data.get('num_bedrooms')
        if num_bedrooms < 0:
            raise ValidationError("Number of bedrooms cannot be negative.")
        return num_bedrooms

    def clean_num_bathrooms(self):
        num_bathrooms = self.cleaned_data.get('num_bathrooms')
        if num_bathrooms < 0:
            raise ValidationError("Number of bathrooms cannot be negative.")
        return num_bathrooms

    def clean_square_footage(self):
        square_footage = self.cleaned_data.get('square_footage')
        if square_footage <= 0:
            raise ValidationError("Square footage must be a positive number.")
        return square_footage

class SubImageForm(ModelForm):
    class Meta:
        model = SubImage
        fields = ['image']  # Field for sub-image

# Create a formset for the SubImage model
SubImageFormSet = modelformset_factory(SubImage, form=SubImageForm, extra=3)  # Adjust 'extra' to the number of initial empty forms you want to display


from django import forms
from .models import Listing
from Location.models import State,LGA,Country
from django import forms
from django import forms
from .models import Listing
from Location.models import State, LGA, Country

class ListingSearchForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Select Country",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors',
            'id': 'country-field'
        })
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),  # Initially empty; dynamically updated via JavaScript
        required=False,
        empty_label="Select State",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-gray-100',
            'id': 'state-field'
        })
    )
    lga = forms.ModelChoiceField(
        queryset=LGA.objects.none(),  # Initially empty; dynamically updated via JavaScript
        required=False,
        empty_label="Select LGA",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-gray-100',
            'id': 'lga-field'
        })
    )
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors',
            'placeholder': 'Enter minimum price'
        })
    )
    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors',
            'placeholder': 'Enter maximum price'
        })
    )
    min_bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors',
            'placeholder': 'Min bedrooms'
        })
    )
    max_bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors',
            'placeholder': 'Max bedrooms'
        })
    )
