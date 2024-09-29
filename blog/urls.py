from django.urls import path

from blog import views

urlpatterns = [
    path('', views.blog_root, name='blog_root'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # path('tag/<int:tag_id>/', views.tag_detail, name='tag_detail'),
]
