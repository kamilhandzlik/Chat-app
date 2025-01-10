from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import *
from .models import *

@login_required
def chat_view(request, chatroom='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom)
    chat_messages = chat_group.chat_messages.all()[:30]   # [:30] ustala liczbę wyświetlonych wiadomości na ostatnie 30 usuń/zmień jeśli chcesz mieć ich więcej/mniej
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'partials/chat_message_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom,
        'chat_group' : chat_group
    }



    return render(request, 'chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('profile', username=username)

    other_user = get_object_or_404(User, username=username)


    existing_chatroom = ChatGroup.objects.filter(
        is_private=True,
        members=request.user
    ).filter(members=other_user).first()

    if existing_chatroom:
        return redirect('chatroom', chatroom=existing_chatroom.group_name)  # Używamy 'chatroom' zamiast 'chatroom_name'


    new_chatroom = ChatGroup.objects.create(
        is_private=True,
        group_name=f"chat_{request.user.username}_{other_user.username}"
    )
    new_chatroom.members.add(request.user, other_user)

    return redirect('chatroom', chatroom=new_chatroom.group_name)


@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form,
    }
    return  render(request, 'create_groupchat.html', context)