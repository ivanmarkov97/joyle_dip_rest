from main_app.api.views import MainDetail
from main_app.models import Relation, ProjectGroup
from chat_app.models import Message
from chat_app.api.serializers import MessageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(MainDetail):
	model_type = Message
	model_serializer = MessageSerializer

	def post(self, request, pk, format=None):
		data = request.data
		sender = int(data['sender'])
		prj_group = int(data['project_group'])
		rel = Relation.objects.get(person=sender, project_group=prj_group)
		if rel:
			serializer = self.model_serializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
		else:
			return Response({"detail": "You can't create message for this group. You're not in this group"})

