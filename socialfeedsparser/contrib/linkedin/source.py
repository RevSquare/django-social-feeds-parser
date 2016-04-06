import datetime
from linkedin import linkedin

from socialfeedsparser.contrib.parsers import ChannelParser, PostParser


class LinkendInSource(ChannelParser):
    """
    Collect class for Facebook.
    """

    name = 'LinkedIn'
    slug = 'linkedin'

    def get_messages_user(self, universal_names, count=20):
        """
        Return posts from user or page feed.

        :param feed_id: id of the page or user to parse.
        :type item: str

        :param count: number of items to retrieve (default 20).
        :type item: int
        """
        return self.get_api().get_company_updates(self.channel.query)['values']

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
        Return linkedin.linkedin.LinkedInApplication
        """
        return linkedin.LinkedInApplication(token=self.channel.user_token)

    def prepare_message(self, message):
        """
        Convert tweets to standard message.

        :param message: message entry to convert.
        :type item: dict
        """
        share = message['updateContent']['companyStatusUpdate']['share']
        l = 'https://www.linkedin.com/hp/updates?topic=%s' \
            % message['updateKey'].split('-')[2]
        return PostParser(
            uid=message['updateKey'].split('-')[2],
            author=message['updateContent']['company']['name'],
            author_uid=message['updateContent']['company']['id'],
            content=share.get('comment', ''),
            date=datetime.datetime.fromtimestamp(
                share['timestamp']/1000.0
            ).strftime('%Y-%m-%d %H:%M:%S'),
            image=share['content'].get(
                'submittedImageUrl', None) or share['content'].get('thumbnailUrl', None),
            link=l
        )
