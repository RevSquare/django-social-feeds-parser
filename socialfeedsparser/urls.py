from django.conf.urls import url

from .views import PostList, save_linkedin_token
from .settings import PAGINATE_BY

urlpatterns = [
    url(r'^$', PostList.as_view(paginate_by=PAGINATE_BY), name="social_feeds_parser"),
    url(r'^linkedin-save-token/', save_linkedin_token, name='linkendin_save_token'),
]
