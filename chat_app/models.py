# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from main_app.models import Project

# Create your models here.

class ProjectGroup(models.Model):
	name = models.CharField(max_length=80)
	description = models.CharField(max_length=80)
	created_at = models.DateField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)

	def __unicode__(self):
		return self.name


class Chat(models.Model):
	project_group = models.OneToOneField(
        ProjectGroup,
        on_delete=models.CASCADE,
        primary_key=True,
    	)

	def __str__(self):
		return str(self.project_group)

	def __unicode__(self):
		return self.project_group

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=160)
	date = models.DateTimeField()
	chat = models.ForeignKey('Chat', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.text)

	def __unicode__(self):
		return self.text
