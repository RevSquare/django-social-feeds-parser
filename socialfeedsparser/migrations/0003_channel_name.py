# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeedsparser', '0002_auto_20150701_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='name',
            field=models.CharField(default=b'', max_length=100, verbose_name="Channel's name", blank=True),
            preserve_default=True,
        ),
    ]
