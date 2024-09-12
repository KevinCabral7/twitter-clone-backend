from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    identificator = models.CharField(max_length=150)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    profile_image = models.URLField(max_length=200, blank=True, null=True)

class Post(models.Model): 
    profile = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280)
    # content_image = models.ImageField()
    like = models.ManyToManyField(Person, related_name='like', blank=True)
    repost = models.ManyToManyField(Person, related_name='repost', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    original_post = models.ForeignKey('self', null=True, blank=True, related_name='reposts', on_delete=models.CASCADE)
