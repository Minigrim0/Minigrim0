from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect

import logging

from blog.models import Post
from blog.forms import BlogPostForm

logger = logging.getLogger(__name__)


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = BlogPostForm
    template_name = 'blog/posts/create.html'
    permission_required = 'blog.create_post'

    def get_initial(self):
        return {
            'date_updated': timezone.now(),
            "slug": "default-slug-that-will-be-changed",
        }


class BlogPostEditView(LoginRequiredMixin, UpdateView):
    form_class = BlogPostForm
    model = Post
    template_name = 'blog/posts/update.html'
    permission_required = 'blog.change_post'

    def get_initial(self):
        return {
            "date_updated": timezone.now(),
            "slug": self.object.slug,
        }


class BlogPostListView(ListView):
    model = Post
    template_name = "blog/posts/list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Post.objects.filter(published=True)


class BlogPostDetailView(DetailView):
    model = Post
    template_name = "blog/posts/detail.html"
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


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/posts/delete.html'
    success_url = '/blog/'
    permission_required = 'blog.delete_post'
    context_object_name = 'post'


def change_post_published_status(request, pk):
    """Changes the publication status of the post depending on the requested action"""

    action = request.GET.get('action', 'toggle')
    post = Post.objects.get(pk=pk)

    match action:
        case "retract":
            post.published = False
        case "publish":
            post.published = True
            post.date_posted = timezone.now()
        case "toggle":
            post.published = not post.published
            if post.published:
                post.date_posted = timezone.now()
        case _:
            logger.error("Unknown action %s", action)

    post.save()
    # Redirect to the previous page or to the blog list
    return redirect(request.META.get('HTTP_REFERER', reverse('blog:blog-list')))
