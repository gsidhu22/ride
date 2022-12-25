from django.urls import path
from users import views as user_views
from . import views as request_views

urlpatterns=[
            path('',request_views.HomeView, name='request-home'),
            path('new/',request_views.AssetCreateView,name='request-create'),
            path('matches/',request_views.MatchView,name='request-match'),
            path('update_status/',request_views.update_status,name='update-status'),
            path('filter/<str:filterby>/',request_views.asset_listing,name='request-filter'),
            path('filter/<str:filterby>/<str:filter2>',request_views.asset_filter_listing,name='request-filter-adv')
            
]
            