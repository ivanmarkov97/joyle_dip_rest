from django.contrib.auth.models import User, Group
from main_app.models import Project, Task, ProjectGroup, Relation
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ('id', 'name', 'description', 'created_at', 'owner')

class ProjectGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectGroup
		fields = ('id', 'name', 'project')

class RelationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Relation
		fields = ('id', 'person', 'project_group')

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('id', 'name', 'description', 'created_at', 'deadline', 'priority', 'is_deleted', 'parent', 'project')
