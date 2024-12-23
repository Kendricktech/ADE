
# URLs configuration (place in urls.py)

from django.urls import path
from .views import (
    ListingCreateView, 
    ListingDetailView, 
    ListingSearchView,
    )
from .views import getLGAs,getStates
app_name = 'listings'

urlpatterns = [
    path('create/', ListingCreateView.as_view(), name='create'),
    path('<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('search/', ListingSearchView.as_view(), name='search'),
    path('load-states/', getStates, name='load_states'),
    path('load-lgas/', getLGAs, name='load_lgas'),
  
]
