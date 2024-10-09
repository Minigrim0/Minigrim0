from django.urls import path

from blog import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog-list'),
    path('new', views.BlogPostCreateView.as_view(), name='post-new'),
    path('p/<str:slug>/', views.BlogPostDetailView.as_view(), name='post-detail'),
    path('p/<str:slug>/edit', views.BlogPostEditView.as_view(), name='post-edit'),
]
