# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialfeedsparser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_uid',
            field=models.CharField(default='', max_length=50, verbose_name='Author id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=50, verbose_name='Author name'),
            preserve_default=True,
        ),
    ]
