# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_receta'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bebida',
        ),
    ]
