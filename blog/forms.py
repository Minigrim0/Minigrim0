from django import forms

from blog.models import Post
from blog.widgets import BlogPostContentWidget

class BlogPostForm(forms.ModelForm):

    class Media:
        css = {
            "all": [
                "https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism-tomorrow.css",
                "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css",
                "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.3/code-input.min.css",
                "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.3/plugins/go-to-line.min.css",
                "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.1/plugins/prism-line-numbers.min.css",
            ]
        }
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js",
            "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.3/code-input.min.js",
            "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.3/plugins/indent.min.js",
            "https://cdn.jsdelivr.net/gh/WebCoder49/code-input@2.3/plugins/go-to-line.min.js",
        ]

    class Meta:
        model = Post
        exclude = ["date_posted", "date_updated"]

        widgets = {
            'slug': forms.HiddenInput(),
            'content': BlogPostContentWidget(),
        }

    def clean(self) -> dict:
        cleaned_data = super().clean()
        print(self.cleaned_data)
        return cleaned_data
