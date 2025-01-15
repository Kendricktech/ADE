from .models import *
from django.views.generic import *
from.forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse

# Agent Views

class Index(TemplateView):
    template_name = 'services/index.html'

class AccountUpgradeView(TemplateView):
    template_name = 'services/account_type.html'


class UnconfirmedView(TemplateView):
    template_name = 'services/unconfirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AgentCreateView(CreateView):
    model = Agent
    form_class=AgentRegistrationForm
    template_name = "services/agent/register.html"
    success_url = reverse_lazy('services:unconfirmed')  # Add this line


    def form_valid(self, form):
        # Set the user field to the current authenticated user
        form.instance.user = self.request.user
        self.request.user.is_agent=True
        return super().form_valid(form)
    
class AgentDetailView(DetailView):
    model = Agent
    template_name = "services/agent/detail.html"

class AgentListView(ListView):
    model = Agent
    template_name = "services/agent/agents.html"

class AgentUpdateView(UpdateView):
    model = Agent
    template_name = "services/agent/update.html"


class AgentDashBoardView(TemplateView):
    template_name = "services/agent/dashboard.html"
    
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated and has an agent profile
        if request.user.is_authenticated:
            if hasattr(request.user, 'agent_profile'):
                agent = request.user.agent_profile
                if agent.status != 'verified':
                    return redirect(reverse('services:unconfirmed'))
        
        return super().get(request, *args, **kwargs)

# Worker Views
class WorkerCreateView(CreateView):
    model = Worker
    form_class=WorkerRegistrationForm   
    template_name = "services/worker/register.html"
    success_url = reverse_lazy('services:unconfirmed')  # Add this line



    def form_valid(self, form):
        # Set the user field to the current authenticated user
        form.instance.user = self.request.user
        self.request.user.is_worker=True

        return super().form_valid(form)
    
    
class WorkerDetailView(DetailView):
    model = Worker
    template_name = "services/worker/detail.html"

class WorkerListView(ListView):
    model = Worker
    template_name = "services/worker/list.html"
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["workers"] =Worker.objects.all()
        print(Worker.objects.all())
        return context
    

class WorkerUpdateView(UpdateView):
    model = Worker
    template_name = "services/worker/update.html"

class WorkerDashBoardView(TemplateView):
    template_name = "services/worker/dashboard.html"
    
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated and has a worker profile
        if request.user.is_authenticated:
            if hasattr(request.user, 'worker_profile'):
                worker = request.user.worker_profile
                if worker.status != 'verified':
                    return redirect(reverse('services:unconfirmed'))
        
        return super().get(request, *args, **kwargs)


# Booking Views
class BookingCreateView(CreateView):
    model = Booking
    template_name = "services/booking/create.html"
    fields = ['worker', 'service_description', 'scheduled_time', 'duration_hours', 'location', 'notes']

class BookingDetailView(DetailView):
    model = Booking
    template_name = "services/booking/detail.html"

class BookingListView(ListView):
    model = Booking
    template_name = "services/booking/list.html"

class BookingUpdateView(UpdateView):
    model = Booking
    template_name = "services/booking/update.html"
    fields = ['status', 'scheduled_time', 'duration_hours', 'notes']

class BookingCancelView(UpdateView):
    model = Booking
    template_name = "services/booking/cancel.html"
    fields = ['status']

    def form_valid(self, form):
        form.instance.status = 'cancelled'
        return super().form_valid(form)



# Review
from django.views.generic import CreateView
from .models import Review
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy

class ReviewCreateView(CreateView):
    model = Review
    template_name = "services/review/create.html"
    fields = ['rating', 'comment']

    def form_valid(self, form):
        # Ensure the correct content type (worker or agent) is set
        object_id = self.kwargs['object_id']
        model_type = self.kwargs['model_type']
        
        if model_type == 'worker':
            from .models import Worker
            content_type = ContentType.objects.get_for_model(Worker)
            object_instance = Worker.objects.get(id=object_id)
        elif model_type == 'agent':
            from .models import Agent
            content_type = ContentType.objects.get_for_model(Agent)
            object_instance = Agent.objects.get(id=object_id)
        else:
            form.add_error(None, 'Invalid model type.')
            return self.form_invalid(form)

        form.instance.customer = self.request.user
        form.instance.content_type = content_type
        form.instance.object_id = object_instance.id
        
        return super().form_valid(form)

    def get_success_url(self):
        model_type = self.kwargs['model_type']
        object_id = self.kwargs['object_id']
        if model_type == 'worker':
            return reverse_lazy('worker-detail', kwargs={'pk': object_id})
        elif model_type == 'agent':
            return reverse_lazy('agent-detail', kwargs={'pk': object_id})

from django.views.generic import ListView
from .models import Review
from django.contrib.contenttypes.models import ContentType

class ReviewListView(ListView):
    model = Review
    template_name = "services/review/list.html"
    context_object_name = 'reviews'

    def get_queryset(self):
        object_id = self.kwargs['object_id']
        model_type = self.kwargs['model_type']
        
        if model_type == 'worker':
            from .models import Worker
            content_type = ContentType.objects.get_for_model(Worker)
            object_instance = Worker.objects.get(id=object_id)
        elif model_type == 'agent':
            from .models import Agent
            content_type = ContentType.objects.get_for_model(Agent)
            object_instance = Agent.objects.get(id=object_id)
        else:
            raise ValueError('Invalid model type.')

        return Review.objects.filter(content_type=content_type, object_id=object_instance.id).order_by('-created_at')

from django.views.generic import UpdateView
from .models import Review
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy

class ReviewUpdateView(UpdateView):
    model = Review
    template_name = "services/review/update.html"
    fields = ['rating', 'comment']

    def get_success_url(self):
        model_type = self.kwargs['model_type']
        object_id = self.kwargs['object_id']
        if model_type == 'worker':
            return reverse_lazy('worker-detail', kwargs={'pk': object_id})
        elif model_type == 'agent':
            return reverse_lazy('agent-detail', kwargs={'pk': object_id})

from django.views.generic import DeleteView
from .models import Review
from django.urls import reverse_lazy

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = "services/review/delete.html"

    def get_success_url(self):
        model_type = self.kwargs['model_type']
        object_id = self.kwargs['object_id']
        if model_type == 'worker':
            return reverse_lazy('worker-detail', kwargs={'pk': object_id})
        elif model_type == 'agent':
            return reverse_lazy('agent-detail', kwargs={'pk': object_id})
