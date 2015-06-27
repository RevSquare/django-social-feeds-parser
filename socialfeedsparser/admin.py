from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from .models import Post, Channel


def get_messages(modeladmin, request, queryset):
    """
    Collects messages from selected sources.
    """
    for source in queryset:
        sc = source.source_class(spoke_source=source)
        sc.collect_messages()
        source.updated = now()
        source.save()

get_messages.short_description = _('Get Messages from selected sources')


class ChannelAdmin(admin.ModelAdmin):
    """
    Admin class for the Channel model.
    """
    list_display = ('query', 'source', 'query_type', 'updated', 'is_active')
    list_filter = ('query', 'source', 'query_type', 'updated', 'is_active')
    actions = [get_messages]
    radio_fields = {"query_type": admin.HORIZONTAL}


class PostAdmin(admin.ModelAdmin):
    """
    Admin class for the Post model.
    """
    list_display = ('channel', 'author', 'content_admin', 'date',
                    'is_active', 'order')
    list_filter = ('is_active', 'channel')
    list_editable = ('is_active', 'order', 'author', 'date')

    def content_admin(self, obj):
        return truncatewords(obj.content, 20)
    content_admin.short_description = _('Post content')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Post, PostAdmin)
