from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from listings.models import Listing
from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)

    # Prevent users from messaging themselves about their own listing
    if item.agent == request.user:
        return redirect('index')
    
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(listing=item, members=request.user).first()
    if existing_conversation:
        return redirect('conversation:detail', pk=existing_conversation.id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            # Create the conversation and associate the listing
            conversation = Conversation.objects.create(listing=item)

            # Add members to the conversation (both user and agent)
            conversation.members.add(request.user)
            conversation.members.add(item.agent)

            # Save the initial conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.agent = request.user  # Assuming the current user is the one sending the message
            conversation_message.save()

            # Redirect to the listing detail page after the conversation is created
            return redirect('listings:detail', pk=listing_id)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    # Fetch all conversations where the current user is a member
    conversations = Conversation.objects.filter(members=request.user)
    return render(request, 'conversation/inbox.html', {'conversations': conversations})


@login_required
def detail(request, pk):
    # Ensure only members of the conversation can access it
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)

    form = ConversationMessageForm(request.POST or None)
    if form.is_valid():
        # Save the new message in the conversation
        conversation_message = form.save(commit=False)
        conversation_message.conversation = conversation
        conversation_message.agent = request.user  # Assuming the current user is sending the message
        conversation_message.save()

        # Redirect to the same conversation detail page after posting the message
        return redirect('conversation:detail', pk=pk)

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
