import hashlib

from instagram.client import InstagramAPI

from .settings import INSTAGRAM_ACCESS_TOKEN
from socialfeedsparser.contrib.parsers import ChannelParser, PostParser


class InstagramSource(ChannelParser):
    """
    Collect class for Instagram.
    """

    name = 'Instagram'
    slug = 'instagram'

    def get_messages_user(self, user_id):
        """
        Return posts from user feed.

        :param user_id: user id of the feed to parse.
        :type item: str

        :param count: number of items to retrieve (default 20).
        :type item: int
        """
        api = self.get_api()
        user = api.user_search(q=user_id)[0].id
        return api.user_recent_media(user_id=user)[0]

    def get_messages_search(self, search):
        """
        Return posts by search param.

        :param search: search string to search for on Instagram.
        :type item: str
        """
        api = self.get_api()
        return api.tag_recent_media(tag_name=search)[0]

    def get_api(self):
        """
        Return authenticated connections with Instagram.
        """
        api = InstagramAPI(access_token=INSTAGRAM_ACCESS_TOKEN)
        return api

    def prepare_message(self, message):
        """
        Convert posts to standard message.

        :param message: message entry to convert.
        :type item: dict
        """
        return PostParser(
            uid=hashlib.sha224(message.id).hexdigest()[:50],
            author=message.user.username,
            content=message.caption,
            date=message.created_time,
            image=message.images['standard_resolution'].url,
            link=message.link
        )
