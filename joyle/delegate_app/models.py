# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from main_app.models import Task

# Create your models here.

class Delegation(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
	date = models.DateTimeField()
	task = models.ForeignKey('main_app.Task', on_delete=models.CASCADE)
	status = models.NullBooleanField(blank=True)

	def __unicode__(self):
		return unicode(self.sender) + u" " + unicode(self.owner)
