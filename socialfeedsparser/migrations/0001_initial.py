# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(default=(b'facebook', b'Facebook'), max_length=50, verbose_name='Social media', choices=[(b'facebook', b'Facebook'), (b'twitter', b'Twitter')])),
                ('limit', models.IntegerField(null=True, verbose_name='Limit', blank=True)),
                ('query', models.CharField(help_text='Enter a search query or user/page id.', max_length=255, verbose_name='Query')),
                ('query_type', models.CharField(default=b'feed', help_text='Note: search is not applicable for Facebook.', max_length=5, verbose_name='Search for:', choices=[(b'feed', 'feed'), (b'search', 'search')])),
                ('periodicity', models.IntegerField(default=60, help_text='Collecting messages periodicy. (In minutes)', verbose_name='Periodicy')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('updated', models.DateTimeField(null=True, verbose_name='Last Updated', blank=True)),
            ],
            options={
                'verbose_name': 'Social feed channel',
                'verbose_name_plural': 'Social feed channels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_uid', models.CharField(verbose_name='ID in the social media source', max_length=255, editable=False)),
                ('link', models.CharField(max_length=255, null=True, verbose_name='Link', blank=True)),
                ('author', models.CharField(max_length=50, verbose_name='Author')),
                ('content', models.TextField(verbose_name='Post content')),
                ('image', models.ImageField(upload_to=b'socialfeedsparser', null=True, verbose_name='Image', blank=True)),
                ('date', models.DateTimeField(null=True, verbose_name='Date', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('like_count', models.PositiveIntegerField(null=True, verbose_name='Like count', blank=True)),
                ('channel', models.ForeignKey(to='socialfeedsparser.Channel')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Social feed post',
                'verbose_name_plural': 'Social feed posts',
            },
            bases=(models.Model,),
        ),
    ]
