from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from common.decorators import ajax_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact
from actions.utils import create_action
from actions.models import Action


# Create your views here.
def user_list(request):
    users = User.objects.all()
    return render(request, 'information/list.html', {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request,
                  'information/detail.html',
                  {'section': 'people',
                   'user': user})

@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.all()
    #actions = Action.objects.exclude(user=request.user)
    '''following_ids = Contact.objects.filter(user_from=request.user).values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)''' #TODO
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request,
                  'information/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'information/update.html', {'form': form})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})

    return JsonResponse({'status': 'ko'})