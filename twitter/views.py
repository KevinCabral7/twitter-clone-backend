from rest_framework import generics
from twitter.models import Post
from twitter.serializers import UserSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Person
from rest_framework.response import Response
from rest_framework import status

class CreateUserView(generics.CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class User(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self): 
        return self.request.user
    
class UserViewSet(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = Person.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Person.objects.all()
        query = self.request.query_params.get('q')
        print(query)
        if query is not None:
            qs = qs.filter(username__icontains=query)
        return qs

class UserInfo(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        identificator = self.kwargs.get('identificator')
        return generics.get_object_or_404(Person, identificator=identificator)  
    
    def post(self, request, identificator):
        user_to_follow = generics.get_object_or_404(Person, identificator=identificator)
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.following.filter(id=user_to_follow.id).exists():
            request.user.following.remove(user_to_follow)
            return Response({"detail": "Successfully unfollowed the user."}, status=status.HTTP_200_OK)

        request.user.following.add(user_to_follow)
        return Response({"detail": "Successfully followed the user."}, status=status.HTTP_200_OK)

class UserProfileUpdate(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_object(self):
        return self.request.user

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(profile=user)


class PostCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(parent=None)
    
    def perform_create(self, serializer):
        if serializer.is_valid(): 
            serializer.save(profile=self.request.user)
        else:
            print(serializer.errors)


class PostDelete(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(profile=user)

class PostInfo(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = generics.get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return obj

class PostLikeList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(like=user)

class PostLike(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk): 
        user = request.user
        post = Post.objects.get(id=pk)
        print(user)
        if user in post.like.all():
            post.like.remove(user)
        else:
            post.like.add(user)

        return Response(post.like.count(), status=status.HTTP_200_OK)

class PostComment(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(parent=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('pk')
        parent = generics.get_object_or_404(Post, id=post_id)
        if serializer.is_valid():
            serializer.save(profile=self.request.user, parent=parent)
        else:
            print(serializer.errors)
        

class PostRepostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(repost=user)

class PostRepost(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        original_post = generics.get_object_or_404(Post, id=pk)
        user = request.user

        # Check if the user has already reposted the post
        repost = Post.objects.filter(profile=original_post.profile, original_post=original_post).first()
        if repost:
            # If the repost exists, remove it
            repost.delete()
            original_post.repost.remove(user)
            return Response(original_post.repost.count(), status=status.HTTP_200_OK)
        else:
            # If the repost does not exist, create a new repost
            new_repost = Post.objects.create(
                profile=original_post.profile,
                content=original_post.content,
                original_post=original_post
            )
            original_post.repost.add(user)
            serializer = self.get_serializer(new_repost)
            return Response(original_post.repost.count(), status=status.HTTP_201_CREATED)       

