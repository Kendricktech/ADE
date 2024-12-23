from django.db import models
from accounts.models import CustomUser
from listings.models import Listing

class Conversation(models.Model):
    listing = models.ForeignKey(Listing, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

    def __str__(self):
        return f"Conversation for {self.listing.title} with {', '.join([member.username for member in self.members.all()])}"
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Track if the message is read by the user

    def __str__(self):
        return f"Message from {self.agent.username} in {self.conversation.listing.title}"
