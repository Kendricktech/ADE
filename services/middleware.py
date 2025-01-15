from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from services.models import Worker, Agent

class UnconfirmedRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):

        # Ensure the user is authenticated
        if request.user.is_authenticated:
            # Check if user has a Worker profile
            if hasattr(request.user, 'worker_profile'):
                worker = request.user.worker_profile
                # If worker's status is not verified, redirect to 'unconfirmed'
                if worker.status != 'verified' and request.path.startswith('/worker/dashboard'):
                    return redirect(reverse('services:unconfirmed'))
            
            # Check if user has an Agent profile
            elif hasattr(request.user, 'agent_profile'):
                agent = request.user.agent_profile
                # If agent's status is not verified, redirect to 'unconfirmed'
                if agent.status != 'verified' and request.path.startswith('/agent/dashboard'):
                    return redirect(reverse('services:unconfirmed'))

        return None
