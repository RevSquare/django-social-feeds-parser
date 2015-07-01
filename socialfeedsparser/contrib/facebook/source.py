import facebook as fbsdk

from socialfeedsparser.contrib.parsers import ChannelParser, PostParser
from .settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET


FACEBOOK_ACCESS_TOKEN = fbsdk.get_app_access_token(
    FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET)


class FacebookSource(ChannelParser):
    """
    Collect class for Facebook.
    """

    name = 'Facebook'
    slug = 'facebook'

    def get_messages_user(self, feed_id, count=20):
        """
        Return posts from user or page feed.

        :param feed_id: id of the page or user to parse.
        :type item: str

        :param count: number of items to retrieve (default 20).
        :type item: int
        """
        return self.get_api().get_connections(feed_id, 'feed')['data']

    def get_messages_search(self, search):
        """
        Return posts by search param.
        THIS API FEATURE HAS BEEN DISABLED BY FACEBOOK

        :param search: search string to search for on twitter.
        :type item: str
        """
        return {}

    def get_api(self):
        """
        Return authenticated connections with fb.
        """
        api = fbsdk.GraphAPI(FACEBOOK_ACCESS_TOKEN)
        return api

    def prepare_message(self, message):
        """
        Convert tweets to standard message.

        :param message: message entry to convert.
        :type item: dict
        """
        l = 'http://www.facebook.com/permalink.php?id=%s&v=wall&story_fbid=%s' \
            % (message['from']['id'], message['id'].split('_')[1])
        return PostParser(
            uid=message['id'],
            author=message['from']['name'],
            author_uid=message['from']['id'],
            content=message.get('message', '') or message.get(
                'description', ''),
            date=message['created_time'],
            image=message.get('picture', None),
            link=l
        )
