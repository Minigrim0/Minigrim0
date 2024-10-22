from django import forms
from django.utils.safestring import mark_safe
from django.forms import widgets


class BlogPostContentWidget(widgets.Widget):
    template_name = "blog/widgets/blog_post_content.html"
