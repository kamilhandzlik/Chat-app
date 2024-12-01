from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]   # [:30] ustala liczbę wyświetlonych wiadomości na ostatnie 30 usuń/zmień jeśli chcesz mieć ich więcej/mniej
    form = ChatmessageCreateForm()

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

    return render(request, 'chat.html', {'chat_messages': chat_messages, 'form': form})
