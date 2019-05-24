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
from actions.models import Action, Message


# Create your views here.
def user_list(request):
    users = User.objects.all()
    tag = request.GET.get('tag')
    if tag and tag != 'None':
        followers = Contact.objects.filter(user_to=request.user).values_list('user_from', flat=True)[:10]
        followers = User.objects.filter(id__in=followers)
        following = Contact.objects.filter(user_from=request.user).values_list('user_to', flat=True)[:10]
        following = User.objects.filter(id__in=following)

        def intersection(lst1, lst2):
            lst3 = [value for value in lst1 if value in lst2]
            return lst3

        if tag == 'Followers':
            users = followers
        elif tag == 'Following':
            users = following
        elif tag == 'Friends':
            users = intersection(followers, following)
    return render(request, 'information/list.html', {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    followers = Contact.objects.filter(user_to=user).values_list('user_from', flat=True)[:10]
    followers = User.objects.filter(id__in=followers)
    following = Contact.objects.filter(user_from=user).values_list('user_to', flat=True)[:10]
    following = User.objects.filter(id__in=following)
    actions = Action.objects.filter(user=user)[:100]
    return render(request,
                  'information/detail.html',
                  {'user': user,
                   'followers': followers,
                   'following': following,
                   'actions': actions})


@login_required
def dashboard(request):
    following = Contact.objects.filter(user_from=request.user).values_list('user_to', flat=True)[:10]
    following = User.objects.filter(id__in=following)
    actions = Action.objects.select_related('user', 'user__profile').prefetch_related('target').filter(
        user__in=following)[
              :100]
    msgs = Message.objects.filter(user_to=request.user)[:100]
    followers = Contact.objects.filter(user_to=request.user).values_list('user_from', flat=True)[:10]
    followers = User.objects.filter(id__in=followers)
    following = Contact.objects.filter(user_from=request.user).values_list('user_to', flat=True)[:10]
    following = User.objects.filter(id__in=following)

    return render(request,
                  'information/dashboard.html',
                  {'actions': actions,
                   'messages': msgs,
                   'followers': followers,
                   'following': following})


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
