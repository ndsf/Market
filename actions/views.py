from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.
@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user_from = request.user
            new_item.save()
            messages.success(request, 'Message sent successfully')
            return redirect('article:post_list')
    else:
        id = request.GET.get('id')
        user = None
        if id and id != 'None':
            user = get_object_or_404(User, id=id)
        if user:
            form = MessageForm(initial={'user_to': user})
        else:
            form = MessageForm()
        return render(request, 'actions/create.html', {'form': form})


@login_required
def conversation(request, id):
    user = get_object_or_404(User, id=id)
    msgs = Message.objects.filter(Q(user_from=request.user, user_to=user) | Q(user_from=user, user_to=request.user))
    return render(request, 'actions/conversation.html', {'user': user, 'messages': msgs})