from django.urls import path

from .views import PostList, PostDetail, AccountDetail, PostSearch, PostCreate, PostUpdate, \
    ReplyList, ReplyCreate, ReplyUpdate, delete_reply, delete_post, accept_reply

urlpatterns = [
    path('board/', PostList.as_view(), name='board'),
    path('board/<int:pk>/', PostDetail.as_view(), name='post'),
    path('account/<int:pk>/', AccountDetail.as_view(), name='account'),
    path('board/search/', PostSearch.as_view(), name='search'),
    path('post/create/', PostCreate.as_view(), name='p_create'),
    path('board/<int:pk>/update/', PostUpdate.as_view(), name='p_update'),
    path('replies/', ReplyList.as_view(), name='replies'),
    path('reply/create/', ReplyCreate.as_view(), name='r_create'),
    path('reply/<int:pk>/update/', ReplyUpdate.as_view(), name='r_update'),
    path('delete/<int:pk>/', delete_reply, name='delete_reply'),
    path('<int:pk>/delete/', delete_post, name='delete_post'),
    path('<int:pk>/accept/', accept_reply, name='accept_reply')

]