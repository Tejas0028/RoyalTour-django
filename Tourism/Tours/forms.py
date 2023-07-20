# Import necessary modules
from django import forms
from .models import *

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'image', 'country', 'city', 'climate', 'language', 'currency', 'timezone', 'itinerary', 'is_popular','days','nights']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the name of the destination'})
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter a description of the destination',
            'rows': 2, 'cols': 60,
            'label': 'Description of the Destination',
        })
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['climate'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the climate of the destination'})
        self.fields['language'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the primary language spoken in the destination'})
        self.fields['currency'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the currency used in the destination'})
        self.fields['timezone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the timezone of the destination'})
        self.fields['days'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the days of the destination'})
        self.fields['nights'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the nights of the destination'})
        self.fields['is_popular'].widget.attrs.update({'class': 'form-check-input', 'style': 'transform: scale(1.8);'})
        self.fields['itinerary'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter a itinerary of the trip',
            'rows': 2, 'cols': 60,
            'label': 'Itinerary of the Destination',
        })
        
