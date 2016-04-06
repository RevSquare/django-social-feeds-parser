# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeedsparser', '0003_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='user_secret',
            field=models.TextField(null=True, blank=True, verbose_name="User Secret"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='user_token',
            field=models.TextField(null=True, blank=True, verbose_name="User Token"),
            preserve_default=False,
        ),
    ]
