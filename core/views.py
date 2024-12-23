from django.shortcuts import render, get_object_or_404
from listings.models import Listing
from conversation.models import ConversationMessage
from accounts.models import CustomUser

def index(request):
    # Get the most recent 5 listings
    listings = Listing.objects.all().order_by('-created_at')[:5]

    # Count unread messages for the logged-in user
    unread_count = (
        ConversationMessage.objects.filter(
            conversation__members=request.user,
            read=False
        ).count()
        if request.user.is_authenticated else 0
    )

    context = {
        'listings': listings,
        'unread_count': unread_count,
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
