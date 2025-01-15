from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from listings.models import Listing
from services.models import Booking, Agent, Worker
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage
from django.db.models import Q

class NewConversationView(LoginRequiredMixin, CreateView):
    model = ConversationMessage
    form_class = ConversationMessageForm
    template_name = 'conversation/new.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Get the appropriate model and item based on item_type
        item_models = {
            'listing': Listing,
            'booking': Booking
        }
        
        self.item_type = self.kwargs['item_type']
        if self.item_type not in item_models:
            messages.error(request, "Invalid conversation type")
            return redirect('conversation:listing')
            
        model = item_models[self.item_type]
        self.item = get_object_or_404(model, pk=self.kwargs['id'])
        
        # Prevent self-messaging
        if self.item.agent and self.item.agent.user == request.user:
            messages.error(request, "You cannot message yourself")
            return redirect('index')
        
        # Check for existing conversation
        if self.item_type == 'listing':
            existing_conversation = Conversation.objects.filter(
                (
                    (Q(sender=request.user) & Q(receiver=self.item.agent)) |
                    (Q(receiver=request.user) & Q(sender=self.item.agent))
                ) & Q(listing=self.item)
            ).first()
        elif self.item_type == 'booking':
            existing_conversation = Conversation.objects.filter(
                (
                    (Q(sender=request.user) & Q(receiver=self.item.worker)) |
                    (Q(receiver=request.user) & Q(sender=self.item.worker))
                ) & Q(booking=self.item)
            ).first()
        
        if existing_conversation:
            return redirect('conversation:detail', pk=existing_conversation.id)

        # Create new conversation
        self.conversation = Conversation.objects.create(
            **{self.item_type: self.item},
            sender=request.user,
            receiver=self.item.agent if self.item_type == 'listing' else self.item.worker
        )
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.item
        context['item_type'] = self.item_type
        return context

    def form_valid(self, form):
        message = form.save(commit=False)
        message.conversation = self.conversation
        
        # Set sender and receiver content types and IDs
        user_type = ContentType.objects.get_for_model(self.request.user)
        if self.item_type == 'listing':
            agent_type = ContentType.objects.get_for_model(self.item.agent)
            message.receiver_type = agent_type
            message.receiver_id = self.item.agent.id
        elif self.item_type == 'booking':
            worker_type = ContentType.objects.get_for_model(self.item.worker)
            message.receiver_type = worker_type
            message.receiver_id = self.item.worker.id
        
        message.sender_type = user_type
        message.sender_id = self.request.user.id
        
        message.save()

        # Add conversation members
        if self.item_type == 'listing':
            self.conversation.members.add(self.request.user, self.item.agent)
        elif self.item_type == 'booking':
            self.conversation.members.add(self.request.user, self.item.worker)
        
        messages.success(self.request, "Message sent successfully")
        return redirect('conversation:detail', pk=self.conversation.id)


class InboxView(LoginRequiredMixin, ListView):
    model = Conversation
    template_name = 'conversation/inbox.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        queryset = (Conversation.objects
            .filter(members=self.request.user)
            .prefetch_related('members', 'messages')
            .select_related('listing', 'booking')
        )
        
        for conversation in queryset:
            conversation.unread_count = conversation.messages.filter(
                read=False
            ).exclude(
                sender_type=ContentType.objects.get_for_model(self.request.user),
                sender_id=self.request.user.id
            ).count()
            
            conversation.latest_message = conversation.messages.first()
            
        return queryset

class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'conversation/detail.html'
    context_object_name = 'conversation'

    def get_queryset(self):
        return (super().get_queryset()
            .prefetch_related('messages', 'members')
            .filter(members=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConversationMessageForm()
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        
        # Mark unread messages as read
        ConversationMessage.objects.filter(
            conversation=self.object,
            read=False
        ).exclude(
            sender_type=ContentType.objects.get_for_model(request.user),
            sender_id=request.user.id
        ).update(read=True)
        
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = self.object
            
            # Set sender content type (current user)
            sender_type = ContentType.objects.get_for_model(request.user)
            message.sender_type = sender_type
            message.sender_id = request.user.id
            
            # Set receiver (the other conversation member)
            other_member = self.object.members.exclude(id=request.user.id).first()
            receiver_type = ContentType.objects.get_for_model(other_member)
            message.receiver_type = receiver_type
            message.receiver_id = other_member.id
            
            message.save()
            
            messages.success(request, "Message sent")
            return redirect('conversation:detail', pk=self.kwargs['pk'])
            
        return self.render_to_response(self.get_context_data(form=form))