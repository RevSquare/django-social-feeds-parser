import re


url_regex = re.compile(r"""
   [^\s]             # not whitespace
   [a-zA-Z0-9:/\-]+  # the protocol and domain name
   \.(?!\.)          # A literal '.' not followed by another
   [\w\-\./\?=&%~#]+ # country and path components
   [^\s]             # not whitespace""", re.VERBOSE)
hashtag_regex = re.compile(r"""
   \#                # a hashmark
   [^\s]*            # not whitespace repeated""", re.VERBOSE)
arobase_regex = re.compile(r"""
   \@                # a hashmark
   [^\s]*            # not whitespace repeated""", re.VERBOSE)


def linkify_url(message):
    """
    Reformats twitter message to replace urls by cliquable links.

    :param message: message to parse.
    :type item: str
    """
    for url in url_regex.findall(message):
        if url.endswith('.'):
            url = url[:-1]
        if 'http://' not in url:
            href = 'http://' + url
        else:
            href = url
        message = message.replace(url, '<a href="%s" target="_blank">%s</a>' % (href, url))

    return message


def linkify_hashes(message):
    """
    Reformats twitter message to replace hashes by cliquable links.

    :param message: message to parse.
    :type item: str
    """
    hashtags = hashtag_regex.findall(message)
    for hashtag in hashtags:
        cleaned_hash = re.sub(r'[^a-zA-Z0-9]+', '', hashtag)
        formated_hashtag = '#%s' % cleaned_hash
        message = message \
            .replace(formated_hashtag,
                     '<a href="https://twitter.com/search?q=%s&src=hash" target="_blank">&#35;%s</a>'\
                     % (cleaned_hash, cleaned_hash))

    return message


def linkify_arobase(message):
    """
    Reformats twitter message to replace hashes by cliquable links.

    :param message: message to parse.
    :type item: str
    """
    arobases = arobase_regex.findall(message)
    for arobase in arobases:
        cleaned_arobase = re.sub(r'[^a-zA-Z0-9]+', '', arobase)
        formated_arobase = '@%s' % cleaned_arobase
        message = message \
            .replace(formated_arobase,
                     '<a href="https://twitter.com/%s" target="_blank">&#64;%s</a>'\
                     % (cleaned_arobase, cleaned_arobase))

    return message


def linkify(message):
    """
    Reformats twitter message to replace urls, hashes and arrobased strings
    by cliquable links.

    :param message: message to parse.
    :type item: str
    """
    message = linkify_url(message)
    message = linkify_hashes(message)
    message = linkify_arobase(message)

    return message


def get_source(slug):
    """
    Return source class from given slug

    :param slug: slug to parse.
    :type item: str
    """
    from .models import SOURCE
    for cls in SOURCE:
        if cls.slug == slug:
            return cls
