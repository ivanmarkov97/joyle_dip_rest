# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Project, Task, ProjectGroup, Relation
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(ProjectGroup)
admin.site.register(Relation)
