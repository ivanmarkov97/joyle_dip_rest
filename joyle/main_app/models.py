# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
	#proj_id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name

class ProjectGroup(models.Model):
	name = models.CharField(max_length=80)
	project = models.ForeignKey('Project', unique=True, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.name

class Relation(models.Model):
	person = models.ForeignKey(User, on_delete=models.CASCADE)
	project_group = models.ForeignKey('ProjectGroup', on_delete=models.CASCADE)

	def __unicode__(self):
		return person	

class Task(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateField()
	deadline  = models.DateField()
	priority = models.PositiveIntegerField(default=0)
	is_deleted = models.BooleanField(default=False)
	parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
	project = models.ForeignKey('Project', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name

