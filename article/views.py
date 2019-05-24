from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm, PostForm, PostUpdateForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action, delete_action
import redis
from django.conf import settings
from django.db.models import Q

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


# Create your views here.

def post_list(request):
    posts = Post.objects.all()

    tag = request.GET.get('tag')
    if tag and tag != 'None':
        if tag == '收藏':
            posts = request.user.posts_liked.all()
        else:
            posts = posts.filter(tags__name__in=[tag])

    paginator = Paginator(posts, 9)
    page = request.GET.get('page')

    form = SearchForm()
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__icontains=query)
            )
        return render(request,
                      'article/search.html',
                      {'form': form,
                       'query': query,
                       'results': results})

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整数，就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果是不存在的页数，而且请求是AJAX请求，返回空字符串
        if request.is_ajax():
            return HttpResponse('')
        # 如果页数超范围，显示最后一页
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'article/list_ajax.html', {'posts': posts, 'tag': tag, 'form': form})
    return render(request, 'article/list.html', {'posts': posts, 'tag': tag, 'form': form})


@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    # increment total post views by 1
    total_views = r.incr('post:{}:views'.format(post.id))
    # increment post ranking by 1
    r.zincrby('post_ranking', post.id, 1)

    # 列出文章对应的所有活动的评论
    comments = post.comments.all()

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            new_comment.author = request.user
            create_action(request.user, 'commented post', post)
            # 将评论数据对象写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 显示相近Tag的文章列表
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_tags = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-updated')[:4]
    return render(request, 'article/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form,
                   'similar_posts': similar_posts, 'total_views': total_views})


def post_share(request, id):
    # 通过id 获取 post 对象
    post = get_object_or_404(Post, id=id)
    sent = False

    if request.method == 'POST':
        # 表单被提交
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 验证表单数据
            cd = form.cleaned_data
            # 发送邮件......
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'lee0709@vip.sina.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'article/share.html', {'post': post, 'form': form})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__icontains=query)
            )
    return render(request,
                  'article/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


@login_required
def post_create(request):
    if request.method == 'POST':
        # 表单被提交
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            # 将当前用户附加到数据对象上
            new_item.author = request.user
            new_item.save()
            create_action(request.user, 'created post', new_item)
            form.save_m2m()
            messages.success(request, 'Post added successfully')
            # 重定向到新创建的数据对象的详情视图
            return redirect(new_item.get_absolute_url())
        else:
            return redirect('article:post_list')
    else:
        # 根据GET请求传入的参数建立表单对象
        form = PostForm(data=request.GET)
        return render(request, 'article/create.html', {'form': form})


@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect(post.get_absolute_url())
    if request.method == 'POST':
        form = PostUpdateForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'Error updating your profile')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
        return render(request, 'article/update.html', {'form': form})


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect(post.get_absolute_url())
    delete_action(post)
    post.delete()
    return redirect('article:post_list')


@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
                create_action(request.user, 'likes', post)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


def post_ranking(request):
    # get post ranking dictionary
    post_ranking = r.zrange('post_ranking', 0, -1, desc=True)[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed posts
    most_viewed = list(Post.objects.filter(
        id__in=post_ranking_ids))
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    return render(request,
                  'article/ranking.html',
                  {'most_viewed': most_viewed})
