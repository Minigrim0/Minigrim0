import logging

import mistune
from django import template
from django.template.loader import render_to_string
from mistune.plugins.task_lists import task_lists
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

logger = logging.getLogger(__file__)
register = template.Library()


class CleanRenderer(mistune.HTMLRenderer):
    # inline level
    def text(self, text):
        return text

    def link(self, text, url, title=None):
        return text

    def image(self, text, url, title=None):
        return text

    def emphasis(self, text):
        return text

    def strong(self, text):
        return text

    def codespan(self, text):
        return text

    def linebreak(self):
        return "<br />"

    def softbreak(self):
        return "<br />"

    def inline_html(self, html):
        return ""

    # block level
    def paragraph(self, text):
        return text + " "

    def heading(self, text, level, **attrs):
        return text + ". "

    def blank_line(self):
        return ""

    def thematic_break(self):
        return "<br />"

    def block_text(self, text):
        return text

    def block_code(self, code, info=None):
        return ""

    def block_quote(self, text):
        return text

    def block_html(self, html):
        return ""

    def block_error(self, text):
        return text

    def list(self, text, ordered, **attrs):
        return text

    def list_item(self, text, **attrs):
        return text

    # provided by strikethrough plugin
    def strikethrough(self, text):
        return text

    # provided by mark plugin
    def mark(self, text):
        return text

    # provided by insert plugin
    def insert(self, text):
        return text

    # provided by subscript plugin
    def subscript(self, text):
        return text

    # provided by abbr plugin
    def abbr(self, text, title):
        return text

    # provided by task_lists plugin
    def task_list_item(self, text, checked=False, **attrs):
        return text

    # provide by table plugin
    def table(self, text):
        return text

    def table_head(self, text):
        return text

    def table_body(self, text):
        return text

    def table_row(self, text):
        return text

    def table_cell(self, text, align=None, head=False):
        return text

    # provide by def_list plugin
    def def_list(self, text):
        return text

    def def_list_head(self, text):
        return text

    def def_list_item(self, text):
        return text

    # provide by math plugin
    def block_math(self, text):
        return text

    def inline_math(self, text):
        return text


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info != "" and info is not None:
            if ":" in info:
                lang, filename = info.split(":")
            else:
                lang = info
                filename = None
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter()
            rendered_code = highlight(code, lexer, formatter)
            lines = len(code.split("\n")) - 1
            result = render_to_string(
                "blog/code_block.html",
                context={
                    "code": rendered_code,
                    "filename": filename,
                    "line_range": range(lines),
                    "lang": lang,
                },
            )
            return result
        else:
            if info is None:
                info = "text"
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = HtmlFormatter()
            return highlight(code, lexer, formatter)


class SimpleHighlight(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info is None:
            info = "text"
        lexer = get_lexer_by_name(info, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


@register.filter
def markdown(value):
    """Returns HTML with code fancy blocks (copy button, line numbers)"""
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer, plugins=[task_lists])
    return markdown(value)


@register.filter
def simple_markdown(value):
    """Returns HTML with colored code blocks"""
    renderer = SimpleHighlight()
    markdown = mistune.Markdown(renderer=renderer, plugins=[task_lists])
    return markdown(value)


@register.filter
def cleaned_markdown(value):
    """Returns pure text, no HTML. Skips code blocks"""
    renderer = CleanRenderer()
    markdown = mistune.Markdown(renderer=renderer, plugins=[task_lists])
    return markdown(value)
