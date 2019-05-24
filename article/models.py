from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from uuslug import slugify
from taggit.managers import TaggableManager


# Create your models here.

class Post(models.Model):
    # STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts_created', on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='images/%Y%m%d/', blank=True, default='default-post.png')
    body = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    # objects = models.Manager()
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments_created', on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
