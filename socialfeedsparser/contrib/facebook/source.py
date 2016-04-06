import facebook as fbsdk

from socialfeedsparser.contrib.parsers import ChannelParser, PostParser
from socialfeedsparser.settings import SOCIALFEEDSPARSER_TIMEOUT
from .settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
try:
    from urllib2 import urlopen
    from urllib import urlencode
except (ImportError):  # for python >= 3.4
    from urllib.request import urlopen
    from urllib.parse import urlencode


def get_app_access_token(app_id, app_secret):
    """Get the access_token for the app.

    This token can be used for insights and creating test users.

    app_id = retrieved from the developer page
    app_secret = retrieved from the developer page

    Returns the application access_token.

    """
    # Get an app access token
    args = {'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret}

    file = urlopen("https://graph.facebook.com/oauth/access_token?" +
                   urlencode(args))
    file_readed = file.read()
    try:
        result = file_readed.split("=")[1]
    except (TypeError):
        result = file_readed.decode("utf-8").split("=")[1]
    finally:
        file.close()
    return result

FACEBOOK_ACCESS_TOKEN = get_app_access_token(
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
        try:
            ret = self.get_api().get_connections(feed_id.encode('utf-8'), 'feed')['data']
        except(fbsdk.GraphAPIError):
            ret = self.get_api().get_connections(feed_id, 'feed')['data']

        return ret

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
        api = fbsdk.GraphAPI(FACEBOOK_ACCESS_TOKEN, timeout=float(SOCIALFEEDSPARSER_TIMEOUT))
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
