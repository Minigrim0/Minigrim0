from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe


class BlogPostContentWidget(widgets.Widget):
    template_name = "blog/widgets/blog_post_content.html"
