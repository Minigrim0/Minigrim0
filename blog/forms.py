from django import forms

from blog.models import Post


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["date_posted", "date_updated"]

        widgets = {
            'content': forms.Textarea(attrs={'rows': 25}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
