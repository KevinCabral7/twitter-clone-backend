from twitter.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Person

class UserSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields= ['id', 'username', 'identificator', 'password', 'post_count','follower_count', 'following_count', 'profile_image']
        extra_kwargs = {'password': {'write_only': True}}

    def get_post_count(self, obj):
        return Post.objects.filter(profile=obj).count()

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        user = Person.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.identificator = validated_data.get('identificator', instance.identificator)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    profile_username = serializers.SerializerMethodField()
    profile_identificator = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    original_post_content = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta: 
        model = Post
        fields = ['id', 'content', 'created_at', 'profile', 'profile_username', 'profile_identificator','profile_image', 'like', 'repost','parent', 'original_post', 'original_post_content', 'comment_count']
        extra_kwargs = {"profile": {"read_only": True}, "original_post": {"read_only": True}}

    def get_profile_username(self, obj):
        return obj.profile.username
    
    def get_profile_identificator(self, obj):
        return obj.profile.identificator
    
    def get_profile_image(self, obj):
        return obj.profile.profile_image
    
    def get_original_post_content(self, obj):
        if obj.original_post:
            return obj.original_post.content
        return None
    
    def get_comment_count(self, parent):
        count = Post.objects.filter(parent=parent)
        return count.count()