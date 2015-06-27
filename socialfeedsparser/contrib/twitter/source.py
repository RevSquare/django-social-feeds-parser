import tweepy

from socialfeedsparser.contrib.parsers import ChannelParser, PostParser
from .settings import (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
                       TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKENS_SECRET)


class TwitterSource(ChannelParser):
    """
    Collect class for tweeter.
    """

    name = 'Twitter'
    slug = 'twitter'

    def get_messages_user(self, user_id, count=20):
        """
        Return tweets from user feed.

        :param user_id: user id of the feed to parse.
        :type item: str

        :param count: number of items to retrieve (default 20).
        :type item: int
        """
        return self.get_api().user_timeline(
            user_id=user_id, count=count,
            include_entities=True, include_rts=True)

    def get_messages_search(self, search):
        """
        Return tweets by search param.

        :param search: search string to search for on twitter.
        :type item: str
        """
        return self.get_api().search(
            q=search,
            count=self.spoke_source.limit)

    def get_api(self):
        """
        Return authenticated connections with twitter.
        """
        oauth = tweepy.OAuthHandler(
            consumer_key=TWITTER_CONSUMER_KEY,
            consumer_secret=TWITTER_CONSUMER_SECRET)
        oauth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKENS_SECRET)
        return tweepy.API(oauth)

    def prepare_message(self, message):
        """
        Convert tweets to standard message.

        :param message: message entry to convert.
        :type item: dict
        """
        # TODO: add getting images from tweet
        # https://dev.twitter.com/docs/tweet-entities

        return PostParser(
            uid=message.id_str,
            author=message.user.name,
            content=message.text,
            date=message.created_at,
            link='https://twitter.com/%s/status/%s' % (
                message.user.screen_name, message.id_str)
        )
