# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name


class Task(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateField()
	deadline  = models.DateField()
	priority = models.PositiveIntegerField(default=0)
	project = models.ForeignKey('Project', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name

