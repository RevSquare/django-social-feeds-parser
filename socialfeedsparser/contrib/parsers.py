import hashlib
import os
import urllib2

from django.core.files.base import ContentFile


class ChannelParser(object):
    """
    Base parser class for all sources (twitter, fb...)
    """
    name = None
    slug = None

    def __init__(self, channel):
        """
        :param channel: models.Channel instance to collect messages for.
        :type item: int
        """
        self.channel = channel

    def collect_messages(self):
        """
        Retrieves and saves message for the models.Channel instance.
        """
        messages = self.get_messages()
        messages = [self.prepare_message(message) for message in messages]
        for message in messages:
            message.save(channel=self.channel)

    def get_messages(self):
        """
        Get a list of messages to process.
        """
        messages = []
        searches = map(lambda x: x.strip(),
                       self.channel.query.split(','))

        for search in searches:
            if self.channel.query_type == self.channel.FEED:
                messages.extend(self.get_messages_user(search))
            else:
                messages.extend(self.get_messages_search(search))

        return messages

    def get_messages_user(self, user_id):
        """
        Must return list of messages from social channel. Depending on search string.
        Overwrite to get list of messages from user account.

        :param user_id: user id of the feed to parse.
        :type item: str
        """
        raise NotImplementedError

    def get_messages_search(self, search):
        """
        Must return list of messages from social channel. Depending on search string.
        Overwrite to get list of messages that are match to search string.

        :param search: search string to search for on twitter.
        :type item: str
        """
        raise NotImplementedError

    def prepare_message(self, message):
        """
        Convert returned datas into standard message.

        :param message: message entry to convert.
        :type item: dict
        """
        raise NotImplementedError


class PostParser(object):
    """
    Manages the formating of posts into database compatible objects for the models.Post class.
    """
    def __init__(self, uid, author=None, author_uid=None, content=None, image=None, date=None, link=None):
        """
        :param uid: ;unique id of the post in the source.
        :type item: str

        :param author: Verbose name of the author who poster the message.
        :type item: str

        :param author_uid: id of the author who poster the message.
        :type item: str

        :param about_us: post content.
        :type item: str

        :param image: image url of the post.
        :type item: str

        :param date: date of publication of the post.
        :type item: str

        :param link: unique url of the post.
        :type item: str
        """
        self.uid = uid
        self.author = author
        self.author_uid = author_uid
        self.content = content
        self.image = image
        self.date = date
        self.link = link

    def save(self, channel):
        """
        Return a Post model class instance.

        :param channel: models.Channel instance to collect messages for.
        :type item: int
        """
        from socialfeedsparser.models import Post

        try:
            sau = Post.objects.get(
                source_uid=self.uid, channel=channel)
        except Post.DoesNotExist:
            sau = Post(
                source_uid=self.uid,
                channel=channel,
                author=self.author,
                author_uid=self.author_uid,
                content=self.content,
                date=self.date,
                link=self.link
            )
            if self.image:
                try:
                    base_file_name = os.path.basename(self.image)
                    file_ext = base_file_name.split('.')[-1]
                    file_name = hashlib.sha224(base_file_name).hexdigest()[:50]
                    file_name += '.' + file_ext
                    downloaded = urllib2.urlopen(self.image).read()
                    image_file = ContentFile(downloaded, name=file_name)
                    sau.image.save(file_name, image_file)
                except Exception:
                    pass

            try:
                sau.save()
            except Exception:
                pass
        return sau
