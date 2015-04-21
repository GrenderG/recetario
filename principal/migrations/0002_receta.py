# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(unique=True, max_length=100)),
                ('ingredientes', models.TextField(help_text=b'Redacta los ingredientes')),
                ('preparacion', models.TextField(verbose_name=b'Preparaci\xc3\xb3n')),
                ('imagen', models.ImageField(upload_to=b'recetario', verbose_name=b'Im\xc3\xa1gen')),
                ('tiempo_registro', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
