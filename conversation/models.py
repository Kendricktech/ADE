from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from listings.models import Listing
from services.models import Booking, Worker, Agent
from django.contrib.auth.models import User as CustomUser

class Conversation(models.Model):
    # Optional foreign key to Listing, as a conversation can happen because of a listing
    listing = models.ForeignKey(Listing, related_name='conversations', on_delete=models.CASCADE, null=True, blank=True)
    
    # Optional foreign key to Booking, as a conversation can also happen because of a booking
    booking = models.ForeignKey(Booking, related_name='conversations', on_delete=models.CASCADE, null=True, blank=True)

    # Members can be either CustomUser, Agent, or Worker
    members = models.ManyToManyField(CustomUser, related_name='conversations', blank=True)  # CustomUser can still be a member
    members = models.ManyToManyField(Agent, related_name='agent_conversations', blank=True)  # Include Agent
    members = models.ManyToManyField(Worker, related_name='worker_conversations', blank=True)  # Include Worker

    # GenericForeignKey to handle multiple types of sender (User, Agent, Worker)
    sender_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    sender_id = models.PositiveIntegerField(null=True)
    sender = GenericForeignKey('sender_type', 'sender_id')

    receiver_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name="conversation_receiver_type")
    receiver_id = models.PositiveIntegerField(null=True)
    receiver = GenericForeignKey('receiver_type', 'receiver_id')

    # Add GenericRelation for reverse querying
    messages = GenericRelation('ConversationMessage', related_query_name='conversation')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

    def __str__(self):
        if self.listing:
            return f"Conversation about {self.listing.title}"
        elif self.booking:
            return f"Conversation about booking {self.booking.id}"
        return "Conversation"
    

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()

    # GenericForeignKey to handle multiple types of sender (User, Agent, Worker)
    sender_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    sender_id = models.PositiveIntegerField(null=True)
    sender = GenericForeignKey('sender_type', 'sender_id')

    receiver_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name="conversation_message_receiver_type")
    receiver_id = models.PositiveIntegerField(null=True)
    receiver = GenericForeignKey('receiver_type', 'receiver_id')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)