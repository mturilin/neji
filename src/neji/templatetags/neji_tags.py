from django import template
from django.conf import settings
import markdown
import os
from path import path

register = template.Library()

@register.simple_tag
def markdown_src(src):
    for dir in settings.TEMPLATE_DIRS:
        filename = path(dir).joinpath(src)
        if filename.exists():
            with open(filename, 'r') as file:
                text = file.read()
                return markdown.markdown(unicode(text, "utf-8"))
    raise RuntimeError("Markdown: file %s is not found in any of the template dirs" % src)