##########################
django-social-feeds-parser
##########################

django-social-feeds-parser is a django application to store and display feed coming from social medias such as:

* facebook
* twitter
* instagram

This library is a fork of Tomasz Roszko's django-spokeaboutus

*******
Install
*******

From Github

.. code-block::  shell-session

    pip install -e git+https://github.com/revsquare/django-social-feeds-parser.git#egg=django_socialfeeds-parser

*****
Setup
*****

settings.py
===========

.. code-block::  python

    INSTALED_APPS = (
        ...
        'socialfeedsparser',
        ...
    )

Configure the social media source you want to trigger. You can of course add you own custom channel source.

.. code-block::  python

    SOCIALFEEDSPARSER_SOURCE = (
        'socialfeedsparser.contrib.twitter',
        'socialfeedsparser.contrib.facebook',
        'socialfeedsparser.contrib.instagram',
        'your.socialfeedsparser.source',
    )

For each service you add, you will need to configure their API accesses:


Facebook
--------

.. code-block::  python

    SOCIALFEEDSPARSER_FACEBOOK_CLIENT_ID = "your app client_id"
    SOCIALFEEDSPARSER_FACEBOOK_CLIENT_SECRET = "your app client secret"

Twitter
-------

.. code-block::  python

    SOCIALFEEDSPARSER_TWITTER_CONSUMER_KEY = "your app consumer key"
    SOCIALFEEDSPARSER_TWITTER_CONSUMER_SECRET = "your app consumer secret key"
    SOCIALFEEDSPARSER_TWITTER_ACCESS_TOKEN = "your app access token"
    SOCIALFEEDSPARSER_TWITTER_ACCESS_TOKEN_SECRET = "your app access token secret"

Instagram
---------

.. code-block::  python

    SOCIALFEEDSPARSER_INSTAGRAM_ACCESS_TOKEN = "your app access token"


urls.py
=======

.. code-block::  python

    urlpatterns = patterns('',
        ...
        url(r'^social-feeds-parser/', include('socialfeedsparser.urls')),
        ...
    )

database
========

.. code-block::  shell-session

    python manage.py syncdb
    python manage.py migrate


*****************
Configure sources
*****************

Each query you setup for a social media is called a "channel". They are configurable from the admin. You can wether parse a user or page feed. Or even use a search query (this functionnality won't work for facebook as the ability to search for posts has been remove from its API).

*******************
Collecting messages
*******************

Run this command (you can of course add it to a cronjob or a scheduled broker):

.. code-block::  shell-session

    python manage.py collect_social_feeds


************
Templatetags
************

A simple template tag is provided to display your content in a widget. You can overwrite it by adding your own 'socialfeedsparser/socialfeed_widget.html' file or by setting up a file path in the SOCIALFEEDSPARSER_TAG_TEMPLATE of your settings. You can alternatively pass the template path as an argument in the template tag in case you have several or if they differ depending on the source.

You can also pass the number of items to display in the template tag.

The first argument to pass is the channel instance you want to display.

.. code-block::  html

    {% load socialfeedsparser_tags %}
    ...
    {% socialfeed_display channel 5 'widgets/twitter.html' %}

*****
Other
*****


channel.get_posts
=================

You can trigger the published posts by order and descending publication date for a channel instance by using the 'get_posts' method. By default it will return 10 posts. You can change this number by passing it as an argument. For exemple, if you want 5 posts:


.. code-block::  python

    channel.get_posts(5)


post.linkified_content
======================

You can use this method to make all urls, hashtags or arobased user names in a message clickable as links:


.. code-block::  html

    {{ post.content }}
    
    "This #hashtag is not linkified."

    {{ post.linkified_content }}
    
    "This <a href="https://twitter.com/search?q=%s&src=hash" target="_blank">##hashtag</a> is linkified for twitter."


****
TODO
****

* use celery to process news
* write tests
