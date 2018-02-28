from django.contrib.auth.models import User, Group
from delegate_app.models import Delegation
from rest_framework import serializers

class DelegateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Delegation
		fields = ('id', 'sender', 'owner', 'date', 'task', 'status')	

	