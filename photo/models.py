from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.http import request
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()

class Post(models.Model):
    objects = models
    published = PublishedManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User, related_name='photo_posts', on_delete=models.CASCADE)
    # body = models.TextField(default="The content goes here")
    picture = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("photo:post_detail", args=[self.id, self.slug])

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

# class Images(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/')
#
#     def __str__(self):
#         return self.post.title + " Image"