# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ProjectGroup, Chat, Message

# Register your models here.

admin.site.register(ProjectGroup)
admin.site.register(Chat)
admin.site.register(Message)
