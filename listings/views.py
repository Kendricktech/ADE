from django.views.generic import CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.db import models
from django.core.exceptions import ValidationError
from django.views import View
from django.views.generic import ListView,CreateView,DetailView
import logging


from .forms import ListingForm, ListingSearchForm
from .models import Listing
from Location.models import State, LGA

# Set up logging
logger = logging.getLogger(__name__)

class ListingCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating new property listings.
    Only authenticated users can access this view.
    """
    model = Listing
    form_class = ListingForm
    template_name = 'listings/create_property.html'
    
    def form_valid(self, form):
        """Handle valid form submission."""
        try:
            # Set the agent to the current user
            form.instance.agent = self.request.user
            
            # Validate the instance
            try:
                form.instance.full_clean()
            except ValidationError as e:
                logger.error(f"Validation error creating listing: {e}")
                messages.error(self.request, "Please correct the errors below.")
                return self.form_invalid(form)
            
            response = super().form_valid(form)
            messages.success(self.request, "Property listing created successfully!")
            return response
            
        except Exception as e:
            logger.error(f"Error creating listing: {str(e)}")
            messages.error(self.request, "An error occurred while creating the listing.")
            return self.form_invalid(form)
    
    def get_success_url(self):
        """Return URL to redirect to after successful creation."""
        return reverse_lazy('listings:listing_detail', kwargs={'pk': self.object.pk})

class ListingDetailView(DetailView):
    """
    View for displaying details of a specific property listing.
    """
    model = Listing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        try:
            context = super().get_context_data(**kwargs)
            # Add additional context data here as needed
            # For example: similar listings, agent info, etc.
            return context
        except Exception as e:
            logger.error(f"Error in listing detail view: {str(e)}")
            messages.error(self.request, "Error retrieving listing details.")
            return context
        
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from .forms import ListingSearchForm
from .models import Listing

class ListingSearchView(ListView):
    model = Listing
    template_name = 'listings/search_listings.html'
    context_object_name = 'listings'
    paginate_by = 12
    form_class = ListingSearchForm
    def get_context_data(self, **kwargs):
    # Call the parent's method to get the default context
        context = super().get_context_data(**kwargs)
        
        # Add custom context data
        context['form'] = self.form_class()  # Assuming `form_class` is defined for the view
        
        return context

# def getModelList(request, model):
#     """
#     Helper function to get all instances of a model and return them as a JSON response.
#     """
#     data_list = list(model.objects.all().values('id', 'name'))  # Get list of ids and names
#     return JsonResponse(data_list, safe=False)
from django.http import JsonResponse
from django.http import JsonResponse
import json

from django.http import JsonResponse
import json
from django.http import JsonResponse
import json


def getStates(request):
    """
    Get states based on country_name (using regex) and return them as a JSON response.
    """
    # Get the raw POST data and parse it as JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    country_name = data.get('country_name')

    if not country_name:
        return JsonResponse({'error': 'Country name is required'}, status=400)

    # Using regex to find country name in the 'Country' model
    states = State.objects.filter(country__name__regex=fr'^{country_name}$')

    # Create the response data
    state_data = [{'id': state.id, 'name': state.name} for state in states]

    return JsonResponse(state_data, safe=False)



from django.http import JsonResponse
import json

def getLGAs(request):
    """
    Get LGAs based on state_name (using regex) and return them as a JSON response.
    """
    try:
        data = json.loads(request.body)  # Parse JSON payload
        print("Data received in getLGAs:", data)  # Debug log
        state_name = data.get('state_name')  # Extract state_name

        if state_name:
            print(f"Searching LGAs for state: {state_name}")  # Debug log
            lgas = LGA.objects.filter(state__name__iregex=fr'^{state_name}$')  # Case-insensitive match
            lga_data = [{'name': lga.name} for lga in lgas]

            print("LGAs found:", lga_data)  # Debug log
            return JsonResponse(lga_data, safe=False)
        else:
            print("No state_name provided")  # Debug log
            return JsonResponse([], safe=False)  # Return an empty list if no state_name is provided
    except json.JSONDecodeError:
        print("Invalid JSON received")  # Debug log
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
