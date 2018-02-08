from rest_framework import serializers
from chat_app.models import ProjectGroup, Chat, Message

class ProjectGrpupSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectGroup
		fields = ('id', 'name', 'description', 'created_at', 'owner', 'project')

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Chat
		fields = ('id', 'project_group')

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('id', 'sender', 'text', 'date', 'chat')
