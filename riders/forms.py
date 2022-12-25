from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile,AssetRequest,TravelInfo
from django.contrib.admin import widgets 


class RideCreateForm(forms.ModelForm):    
    time = forms.DateTimeField(widget = forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model=TravelInfo
        fields=['transport_from','transport_to','time','travel_medium','flexible_timings','asset_quantity']

