from django.urls import path
from users import views as user_views
from . import views as rider_views

urlpatterns=[
                path('',rider_views.HomeView, name='riders-home'),
                path('new/',rider_views.RideCreateView,name='ride-create')
            ]