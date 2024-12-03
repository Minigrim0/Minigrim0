from django.urls import path

from blog import autocomplete, views

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blog-list"),
    path("new", views.BlogPostCreateView.as_view(), name="post-new"),
    path("p/<str:slug>/", views.BlogPostDetailView.as_view(), name="post-detail"),
    path("p/<str:slug>/edit", views.BlogPostEditView.as_view(), name="post-edit"),
    path("p/<str:slug>/delete", views.BlogPostDeleteView.as_view(), name="post-delete"),
    path("p/<str:pk>/publish", views.change_post_published_status, name="post-publish"),
    path(
        "p/t/autocomplete",
        autocomplete.TagAutocomplete.as_view(),
        name="tag-autocomplete",
    ),
]
