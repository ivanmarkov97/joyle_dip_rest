# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
	#proj_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateTimeField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name

class ProjectGroup(models.Model):
	name = models.CharField(max_length=80)
	created_at = models.DateTimeField()
	project = models.ForeignKey('Project', unique=True, on_delete=models.CASCADE)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.name

class Relation(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField()
	project_group = models.ForeignKey('ProjectGroup', on_delete=models.CASCADE)

	def __unicode__(self):
		return unicode(self.person)	

class Task(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateTimeField()
	deadline  = models.DateTimeField()
	priority = models.PositiveIntegerField(default=0)
	position = models.PositiveIntegerField(default=0)
	parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
	project = models.ForeignKey('Project', on_delete=models.CASCADE)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name

