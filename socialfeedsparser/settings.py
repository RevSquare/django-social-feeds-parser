from django.conf import settings

PAGINATE_BY = getattr(settings, 'SOCIALFEEDSPARSER_PAGINATE_BY', 6)

DEFAULT_SOURCE = (
    'socialfeedsparser.contrib.twitter',
    'socialfeedsparser.contrib.facebook',
    'socialfeedsparser.contrib.instagram',
)

SOCIALFEEDSPARSER_SOURCE = getattr(settings, 'SOCIALFEEDSPARSER_SOURCE', DEFAULT_SOURCE)
SOCIALFEEDSPARSER_TAG_TEMPLATE = getattr(settings, 'SOCIALFEEDSPARSER_TAG_TEMPLATE', '')
