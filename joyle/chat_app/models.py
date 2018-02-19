# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from main_app.models import ProjectGroup

# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField()
	group_project = models.ForeignKey('main_app.ProjectGroup', on_delete=models.CASCADE)

	def __unicode__(self):
		return self.text
