from django import template
from django.template.loader import render_to_string
import mistune
from mistune.plugins.task_lists import task_lists
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import logging

logger = logging.getLogger(__file__)
register = template.Library()

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info = None):
        logger.info("Info: %s", info)

        if not info:
            return f"""
```
{mistune.escape(code)}
```
            """

        if ":" in info:
            lang, filename = info.split(":")
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter()
            rendered_code = highlight(code, lexer, formatter)
            lines = len(code.split("\n"))
            return render_to_string("blog/code_block.html", {code: rendered_code, filename: filename})
        else:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = HtmlFormatter()
            return highlight(code, lexer, formatter)

@register.filter
def markdown(value):
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer, plugins=[task_lists])
    return markdown(value)
