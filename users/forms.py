from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile,AssetRequest,TravelInfo
from django.contrib.admin import widgets 

user_choices=[('',''),('rider','Rider'),('requester','Requester')]
class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']
    
class AssetRequestForm(forms.ModelForm):
    class Meta:
        model=AssetRequest
        fields='__all__'

class AssetCreateForm(forms.ModelForm):    
    time = forms.DateTimeField(widget = forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model=AssetRequest
        fields=['transport_from','transport_to','time','flexible_timings','asset_type','asset_sensitivity','asset_quantity','deliver_to']


class RideCreateForm(forms.ModelForm):    
    time = forms.DateTimeField(widget = forms.widgets.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model=TravelInfo
        fields=['transport_from','transport_to','time','travel_medium','flexible_timings','asset_quantity']


class ProfileUpdateForm(forms.ModelForm):
    type= forms.CharField(label='What is the User type?', widget=forms.Select(choices=user_choices))
    class Meta:
        model=Profile
        fields=['type']



