from django.conf.urls import patterns, url

from .views import PostList
from .settings import PAGINATE_BY

urlpatterns = patterns(
    '',
    url(r'^$', PostList.as_view(paginate_by=PAGINATE_BY), name="social_feeds_parser"),
)
