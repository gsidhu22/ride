from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import AssetCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import AssetRequest,TravelInfo
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django_tables2.utils import A
from django_tables2 import RequestConfig
from django.utils import timezone


class MyColumn(tables.Column): 
    empty_values = list() 
    def render(self, value, record): 
        return mark_safe('<button id="%s" class="btn btn-info">Apply</button>' % escape(record))


class RequestTable(tables.Table):
    class Meta:
        model=AssetRequest
        attrs = {'class': 'table table-sm'}




class NameTable(tables.Table):
    transport_from = tables.Column(verbose_name='From')
    transport_to=tables.Column(verbose_name='To')
    time=tables.Column(verbose_name='Date and Time')
    travel_medium=tables.Column(verbose_name='Travel Medium')
    asset_quantity=tables.Column(verbose_name='Asset Quantity')
    rider=tables.Column(verbose_name='Rider')
    applied=tables.BooleanColumn(verbose_name='Application Status')
    #acciones = tables.TemplateColumn(template_code='<a href="" class="btn btn-success">Apply</a>')
    #applieded=MyColumn(verbose_name='Application Statoos')
    Apply = tables.LinkColumn('item_edit', args=[A('ride_id'),A('request_id')],orderable=False, text='Apply ',empty_values=())
    class Meta:
        attrs = {'class': 'table table-sm'}
    
def render_edit(self):
    return 'Edit'

def item_edit(self,ride_id,request_id):
    print(f"ride_id is {ride_id} and  request_id is {request_id}")
    ride_obj=TravelInfo.objects.get(id=ride_id)
    print(f" request is {AssetRequest.objects.get(id=request_id)}")
    ride_obj.applicants.add(AssetRequest.objects.get(id=request_id))
    
    return redirect('request-match')
# Create your views here.
def HomeView(request):
    try:
        if request.user.profile.type=='requester':
            table=RequestTable(AssetRequest.objects.filter(requester=request.user))
            RequestConfig(request,paginate={"per_page": 5}).configure(table)         
            return render(request,'requests/home.html',{'requests':table})
            #return render(request,'requests/home.html',{'requests':AssetRequest.objects.filter(status='EXPIRED')})
    
    except:
        return render(request,'requests/home.html')
    
def asset_listing(request,filterby):
    if filterby=='PENDING' or filterby=='EXPIRED':
        table = RequestTable(AssetRequest.objects.filter(status=filterby,requester=request.user))
        RequestConfig(request,paginate={"per_page": 5}).configure(table)  
        status=True
    else:
        table = RequestTable(AssetRequest.objects.filter(asset_type=filterby,requester=request.user))
        RequestConfig(request,paginate={"per_page": 5}).configure(table)  
        status=False
    #table.paginate(page=request.GET.get("page", 1), per_page=5)
    return render(request, "requests/filter.html", {"table": table,'initial':filterby,'status':status})

def asset_filter_listing(request,filterby,filter2):
    if filterby=='PENDING' or filterby=='EXPIRED':
        table = RequestTable(AssetRequest.objects.filter(status=filterby,requester=request.user,asset_type=filter2))
        status_first=True
        RequestConfig(request,paginate={"per_page": 5}).configure(table)  
    else:
        table = RequestTable(AssetRequest.objects.filter(asset_type=filterby,requester=request.user,status=filter2))
        status_first=False
        RequestConfig(request,paginate={"per_page": 5}).configure(table)  
    table.paginate(page=request.GET.get("page", 1), per_page=10)
    print(status_first)
    return render(request, "requests/filter2.html", {"table": table,'status':status_first,'initial':filterby,'final':filter2})

def MatchView(request):
    myreqs=AssetRequest.objects.filter(requester=request.user)
    rides=TravelInfo.objects.all()
    matches=[]
    for i in myreqs:
        for j in rides:
            print(f"i: {i} j: {j} \n")
            if i.transport_from==j.transport_from and i.transport_to==j.transport_to:
                
                if i.time.date()==j.time.date():
                    #matches.append(j.id)
                    print(f"Requester Date: {i.time.date()} and Rider Time: {j.time.date()}")
                    temp_dict={'transport_from':j.transport_from,
                                'transport_to':j.transport_to,
                                'time':j.time,
                                'travel_medium':j.travel_medium,
                                'asset_quantity':j.asset_quantity,
                                'rider':j.rider.username,
                                'ride_id':j.id,
                                'request_id':i.id
                                }
                    if i in j.applicants.all():
                        temp_dict['applied']=True
                    else:
                        temp_dict['applied']=False
                    
                    print(f"This is the dict being appended {temp_dict}, and matches beforehand is {matches}")
                    matches.append(temp_dict.copy())

    
    print(f"len of matches is {len(matches)},\nmatches is \n {matches}")
    names=NameTable(matches)
    RequestConfig(request,paginate={"per_page": 5}).configure(names)  
    context={'requests':names}
    return render(request,'requests/requests.html',context)



        
@login_required
def AssetCreateView(request,*args,**kwargs):
    if request.method== 'POST':
        form=AssetCreateForm(request.POST)        
        if form.is_valid():
            profile=form.save(commit=False)
            profile.requester=request.user
            if profile.time<timezone.now():
                print("Expired")
                profile.status='EXPIRED'
            profile.save(*args,**kwargs)             
            
            messages.success(request,f"Asset Transport Request Created Successfully.")
            return redirect('users-home')
    else:
        form=AssetCreateForm()
        
    return render(request,'users/assetrequest_form.html',{'form':form})



def update_status(request):
    reqs=AssetRequest.objects.all()
    for i in reqs:
        if i.time<timezone.now():
            i.status='EXPIRED'
        else:
            i.status='PENDING'
        i.save()
    return redirect('users-home')