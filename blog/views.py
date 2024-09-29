from django.shortcuts import HttpResponse, render
from blog.models import Post


def blog_root(request) -> HttpResponse:
    """Returns a list of published posts"""

    posts = Post.objects.filter(published=True).order_by('-date_posted')

    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id: int) -> HttpResponse:
    """Returns a single post if existing andd published, 404 otherwise"""

    post = Post.objects.get(pk=post_id)
    if post.published is False:
        return HttpResponse(b"Post not found", status=404)

    return render(request, 'blog/post_detail.html', {'post': post})
