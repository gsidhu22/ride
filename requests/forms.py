from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import AssetRequest
from django.contrib.admin import widgets 




class AssetCreateForm(forms.ModelForm):    
    time = forms.DateTimeField(widget = forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model=AssetRequest
        fields=['transport_from','transport_to','time','flexible_timings','asset_type','asset_sensitivity','asset_quantity','deliver_to']

