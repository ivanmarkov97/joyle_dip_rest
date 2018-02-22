# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
from django.contrib.auth.models import User
from main_app.models import ProjectGroup
from main_app.models  import Relation

# Create your models here.

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField()
	project_group = models.ForeignKey('main_app.ProjectGroup', on_delete=models.CASCADE)

	def __unicode__(self):
		return self.text

	@classmethod
	def load_messages(cls, usr, date):
		return cls.objects.all().filter(sender=usr).filter(date__gte=date)
	