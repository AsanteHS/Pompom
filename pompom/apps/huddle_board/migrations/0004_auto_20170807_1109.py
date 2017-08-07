# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-07 15:09
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('huddle_board', '0003_board_draw_pile'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardsection',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='cardsection',
            name='contents',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='contents'),
        ),
    ]
