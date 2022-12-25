from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm,AssetCreateForm,RideCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django_tables2 as tables
from django_tables2 import RequestConfig
from users.models import AssetRequest,TravelInfo
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class RequestTable(tables.Table):
    class Meta:
        model=AssetRequest
        attrs = {'class': 'table table-sm'}

class RideTable(tables.Table):
    class Meta:
        model=TravelInfo
        attrs = {'class': 'table table-sm'}


# Create your views here.
def HomeView(request):
    req_table=RequestTable(AssetRequest.objects.all())
    ride_table=RideTable(TravelInfo.objects.all())
    RequestConfig(request).configure(ride_table)
    RequestConfig(request).configure(req_table)   
    context={'requests': req_table,'rides':ride_table}
    return render(request,'users/home.html',context)





def register(request):    
    if request.method== 'POST':
        form=UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()              
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            messages.success(request,f"Your Account is created successfuly. Login Now.")
            return redirect('profile')
    else:
        form=UserRegisterForm()
        form2=ProfileUpdateForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid():
            # and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request,f"Profile Updated successfuly.")
            return redirect('profile')

    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':user_form,
        'p_form':profile_form}
    
    return render(request,'users/profile.html',context)


