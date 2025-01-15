from django.shortcuts import render, get_object_or_404
from listings.models import Listing
from conversation.models import ConversationMessage
from accounts.models import CustomUser
from services.models import Booking
from listings.models import Listing
from django.views.generic import TemplateView

def index(request):
    # Get the most recent 5 listings
    listings = Listing.objects.all().order_by('-created_at')[:5]

  

    context = {
        'listings': listings,
    }

    return render(request, 'core/index.html', context=context)

def agents_list(request):
    # Get all agents from CustomUser where is_agent is True
    agents = CustomUser.objects.filter(is_agent=True)

    context = {
        'agents': agents,
    }

    return render(request, 'core/agents_list.html', context=context)

def services(request):
    return render(request, 'core/services.html')

def agents_listing(request, id):
    # Fetch the agent based on the id
    agent = get_object_or_404(CustomUser, id=id, is_agent=True)
    
    # Get listings associated with the agent
    listings = Listing.objects.filter(agent=agent)
    
    # Pass agent and listings to the template
    context = {
        'agent': agent,
        'listings': listings,
    }

    return render(request, 'core/agent_listing.html', context=context)


class DashBoardView(TemplateView):
    template_name='core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookings"] = Booking.objects.filter(customer=self.request.user)
        context["listings"] = Listing.objects.filter(taker=self.request.user)

        return context
    