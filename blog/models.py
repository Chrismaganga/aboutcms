from site import USER_BASE
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
# from datetime import datetime, timezone



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.FileField(upload_to='media')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ('-publish', )

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug]
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.FileField(upload_to='media')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


    # @property
    # def age(self):
    #     return datetime.now(tz=timezone.utc) - self.created_at

    # @property
    # def age_days(self):
    #     return self.age.days

    # @property
    # def age_seconds(self):
    #     return self.age.seconds

