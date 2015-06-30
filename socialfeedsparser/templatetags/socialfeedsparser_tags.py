# -*- coding: utf-8 -*-
"""
Template tags
"""
from django import template
from django.utils.safestring import mark_safe

from .models import Channel
from .settings import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def socialfeed_display(context, channel, count=10,
                       template=settings.SOCIALFEEDSPARSER_TAG_TEMPLATE):
    """
    Returns a simple list of post for a channel:

    :param channel: models.Channel instance to return messages for.
    :type item: obj

    :param count: number of items to display.
    :type item: int

    :param template: specifies a template to use.
    :type item: str

    Usage exemple:

    {% socialfeed_display channel 5 'widgets/twitter.html' %}
    """
    assert isinstance(channel, Channel)

    if not template:
        template = 'socialfeedsparser/socialfeed_widget.html'

    tmpl = template.loader.get_template(template)
    context.update({
        'channel': channel,
        'posts': channel.get_posts(count)
    })
    content = tmpl.render(template.Context(context))

    return mark_safe(content)
