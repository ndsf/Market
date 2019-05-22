from django import template
from information.models import Contact

register = template.Library()


@register.simple_tag
def followers_count(user):
    return Contact.objects.filter(user_to=user).count()


@register.simple_tag
def show_follow(request_user, user):
    if Contact.objects.filter(user_from=request_user, user_to=user).exists():
        return 'Unfollow'
    else:
        return 'Follow'


@register.simple_tag
def follow_action(request_user, user):
    if Contact.objects.filter(user_from=request_user, user_to=user).exists():
        return 'unfollow'
    else:
        return 'follow'

@register.simple_tag
def follow_color(request_user, user):
    if Contact.objects.filter(user_from=request_user, user_to=user).exists():
        return 'w3-black'
    else:
        return 'w3-light-gray'