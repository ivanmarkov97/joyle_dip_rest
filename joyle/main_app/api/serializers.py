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
		#fields = ('id', 'name', 'description', 'created_at', 'owner')
		fields = ('__all__')

class ProjectGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectGroup
		fields = ('__all__')

class RelationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Relation
		fields = ('__all__')

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		#fields = ('id', 'name', 'description', 'created_at', 'deadline', 'priority', 'is_deleted', 'parent', 'project')
		fields = ('__all__')
