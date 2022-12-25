from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RideCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django_tables2 as tables
from users.models import AssetRequest,TravelInfo
from django_tables2 import RequestConfig

class RideTable(tables.Table):
    class Meta:
        model=TravelInfo
        attrs = {'class': 'table table-sm'}
def HomeView(request):
    try:
        if request.user.profile.type=='rider':
            table=RideTable(TravelInfo.objects.filter(rider=request.user))
            RequestConfig(request,paginate={'per_page':5}).configure(table)
            return render(request,'riders/home.html',{'requests':table})
    except:
        return render(request,'riders/home.html')





@login_required
def RideCreateView(request,*args,**kwargs):
    if request.method== 'POST':
        form=RideCreateForm(request.POST)        
        if form.is_valid():
            profile=form.save(commit=False)
            profile.rider=request.user
            profile.save(*args,**kwargs)             
            
            messages.success(request,f"Ride Created Successfully.")
            return redirect('users-home')
    else:
        form=RideCreateForm()
        
    return render(request,'riders/create_ride.html',{'form':form})

