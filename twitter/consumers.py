import json
from channels.generic.websocket import AsyncConsumer
import jwt
from Api import settings
from twitter.serializers import UserSerializer
from django.contrib.auth.models import AnonymousUser
from .serializers import UserSerializer, PostSerializer
from channels.db import database_sync_to_async
from .models import Person, Post
from django.shortcuts import get_object_or_404

class PostConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })
        print("WebSocket connection accepted")

    
    async def websocket_disconnect(self, event):
        pass

    async def websocket_receive(self, event):
        message = event['text']
        data = json.loads(message)
        action = data.get('action')
        content = data.get('data')
        parent =data.get('parent')

        if action == 'auth':
            token = content
            self.user = await self.get_user_from_jwt(token)


        if action == 'create_user':
            await self.create_user(content)
        elif action == 'get_user':
            await self.get_user_info()
        elif action == 'follow_user':
            await self.follow_user(content)
        elif action == 'create_post':
            await self.create_post(content, parent)
        elif action == 'like_post':
            await self.like_post(content)
        elif action == 'repost':
            await self.repost(content)
        elif action == 'delete':
            await self.delete(content)
    async def create_user(self, data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            await database_sync_to_async(serializer.save)()
            await self.send(text_data=json.dumps(serializer.data))
        else:
            await self.send(text_data=json.dumps(serializer.errors))

    async def get_user_info(self):
        serializer = UserSerializer(self.user)
        await self.send(text_data=json.dumps(serializer.data))

    async def follow_user(self, identificator):
        user_to_follow = await database_sync_to_async(get_object_or_404)(Person, identificator=identificator)
        if user_to_follow == self.user:
            await self.send(text_data=json.dumps({"detail": "You cannot follow yourself."}))
            return

        if await database_sync_to_async(self.user.following.filter(id=user_to_follow.id).exists)():
            await database_sync_to_async(self.user.following.remove)(user_to_follow)
            await self.send(text_data=json.dumps({"detail": "Successfully unfollowed the user."}))
        else:
            await database_sync_to_async(self.user.following.add)(user_to_follow)
            await self.send(text_data=json.dumps({"detail": "Successfully followed the user."}))

    async def create_post(self, content, parent):

        serializer = PostSerializer(data=content)
        print(parent)
        if parent != None:
            parent = await database_sync_to_async(Post.objects.get)(id=parent)
        print(parent)
        if serializer.is_valid():
            if (parent):
                await database_sync_to_async(serializer.save)(profile=self.user, parent=parent)
            else:
                await database_sync_to_async(serializer.save)(profile=self.user)
            
            
            await self.send({
            "type": "websocket.send",
            "text": json.dumps(serializer.data), 
            'action': "create_post"
        })
        else:
            await self.send({
            "type": "websocket.send",
            "text": json.dumps(serializer.errors)
        })

    async def like_post(self, content):
        post = await database_sync_to_async(Post.objects.get)(id=content["post_id"])
        if await database_sync_to_async(post.like.filter)(id=self.user.id):
            await database_sync_to_async(post.like.remove)(self.user)
        else:
            await database_sync_to_async(post.like.add)(self.user)

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(post.like.count())
        })

    async def repost(self, content):
        original_post = await database_sync_to_async(Post.objects.get)(id=content["post_id"])
        repost = await database_sync_to_async(Post.objects.filter(profile=original_post.profile, parent=original_post).first)()
        if repost:
            await database_sync_to_async(repost.delete)()
            await database_sync_to_async(original_post.repost.remove)(self.user)
            await self.send({
            "type": "websocket.send",
            "text": json.dumps('Repost removed.'),
        })
        else:
            new_repost = await database_sync_to_async(Post.objects.create)(
                profile=self.user,
                content=original_post.content,
                parent=original_post
            )
            await database_sync_to_async(original_post.repost.add)(self.user)
            serializer = PostSerializer(new_repost)
            await self.send({
            "type": "websocket.send",
            "text": json.dumps(serializer.data)
        })

    async def delete(self, content):
        post_to_delete = await database_sync_to_async(Post.objects.get)(id=content["post_id"])
        if post_to_delete:
            await database_sync_to_async(post_to_delete.delete)()
        await self.send({
            "type": "websocket.send",
            "text": json.dumps('post deleted')
        })

    @database_sync_to_async
    def get_user_from_jwt(self, token):
        try:
            token_bytes = token.encode('utf-8')
            payload = jwt.decode(token_bytes, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = Person.objects.get(id=user_id)
            return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return AnonymousUser()