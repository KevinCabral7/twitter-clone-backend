from django.contrib import admin

# Register your models here.
from twitter.models import Post, Person
from django.contrib import admin

admin.site.register(Post)
admin.site.register(Person)
