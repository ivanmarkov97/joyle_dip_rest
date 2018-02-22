from main_app.api.views import MainDetail
from chat_app.models import Message
from chat_app.api.serializers import MessageSerializer
from rest_framework import viewsets

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetail(MainDetail):
	model_type = Message
	model_serializer = MessageSerializer
