from django.shortcuts import HttpResponse, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse

from blog.models import Post
from blog.forms import BlogPostForm



class BlogPostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Post.objects.filter(published=True)


class BlogPostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('view_post', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BlogPostForm(initial={
            'project': self.object,
            'author': self.request.user
        })
        return context
