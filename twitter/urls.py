from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.User.as_view(), name='self-user-info'),
    path('user/posts', views.PostList.as_view(), name='self-user-posts'),
    path('user/reposts/', views.PostRepostList.as_view(), name='reposts-list'),
    path('user/likes/', views.PostLikeList.as_view(),name='likes-list'),
    path('user/update', views.UserProfileUpdate.as_view(), name='user-profile-update'),
    path(r'search', views.UserViewSet.as_view(), name="search"),
    path('user/<str:identificator>/', views.UserInfo.as_view(), name='user-info'),
    path('posts/', views.PostCreate.as_view(), name='posts'),
    path('post/create', views.PostCreate.as_view(), name='post-create'),
    path('post/view/<int:pk>/',views.PostInfo.as_view(), name='view-post'),
    path('post/delete/<int:pk>',views.PostDelete.as_view(), name='delete-post'),
    path('post/like/<int:pk>',views.PostLike.as_view(), name='like-post'),
    path('post/comment/<int:pk>',views.PostComment.as_view(), name='comment-post'),
    path('post/repost/<int:pk>', views.PostRepost.as_view(), name='post-repost'),
]