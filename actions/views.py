from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


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
