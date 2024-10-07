from django.urls import path

from blog import views

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog-list'),
    path('new', views.BlogPostCreateView.as_view(), name='post-new'),
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/edit', views.BlogPostEditView.as_view(), name='post-edit'),
]
