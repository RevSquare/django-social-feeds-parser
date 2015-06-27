from django.db import models
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from .managers import PostManager, ChannelManager
from .settings import SOCIALFEEDSPARSER_SOURCE

# load all sources
from .utils import get_source

SOURCE = [import_module(s).SOCIALFEEDSPARSER_SOURCE for s in SOCIALFEEDSPARSER_SOURCE]
SOURCE_CHOICES = [(s.slug, s.name) for s in SOURCE]


class Channel(models.Model):
    """
    Model storing rules on how to parse a source.
    """
    FEED = 'feed'
    SEARCH = 'search'
    QUERY_TYPE = (
        (FEED, _('feed')),
        (SEARCH, _('search'))
    )

    source = models.CharField(_('Social media'), max_length=50, choices=SOURCE_CHOICES, default=SOURCE_CHOICES[0])
    limit = models.IntegerField(_('Limit'), null=True, blank=True)
    query = models.CharField(_('Query'), max_length=255, help_text=_('Enter a search query or user/page id.'))
    query_type = models.CharField(_('Search for:'), choices=QUERY_TYPE, default=FEED, max_length=5,
                                  help_text=_('Note: search is not applicable for Facebook.'))

    periodicity = models.IntegerField(_('Periodicy'), default=60,
                                      help_text=_('Collecting messages periodicy. (In minutes)'))
    is_active = models.BooleanField(_('Is Active'), default=True)
    updated = models.DateTimeField(_('Last Updated'), null=True, blank=True)

    objects = ChannelManager()

    class Meta:
        verbose_name = _('Social feed channel')
        verbose_name_plural = _('Social feed channels')

    def __unicode__(self):
        return self.get_source_display()

    def can_update(self):
        """
        Return True if source is possible to update
        """
        current = now()
        return self.is_active and (self.updated is None or current > self.updated)

    @property
    def source_class(self):
        return get_source(self.source)


class Post(models.Model):
    """
    Model storing posts of stored sources in SpokeSource.
    """
    source_uid = models.CharField(_('ID in the social media source'), max_length=255, editable=False)
    channel = models.ForeignKey(Channel)
    link = models.CharField(_('Link'), null=True, blank=True, max_length=255)

    author = models.CharField(_('Author'), max_length=50)
    content = models.TextField(_('Post content'))
    image = models.ImageField(
        _('Image'), upload_to='socialfeedsparser', null=True, blank=True)
    date = models.DateTimeField(_('Date'), null=True, blank=True)
    order = models.IntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    like_count = models.PositiveIntegerField(_('Like count'), null=True,
                                             blank=True)

    objects = PostManager()

    class Meta:
        verbose_name = _('Social feed post')
        verbose_name_plural = _('Social feed posts')
        ordering = ('order',)

    def __unicode__(self):
        return u'%s - %s' % (self.source, self.author)
