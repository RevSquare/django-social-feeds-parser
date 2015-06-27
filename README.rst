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

    pip install -e git+https://github.com/revsquare/django-social-feeds-parser.git#egg=django_socialfeeds-parser.git

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



TODO:
-----

* use celery to process news
* wrote tests
