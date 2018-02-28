from main_app.api.views import MainDetail
from delegate_app.models import Delegation
from rest_framework.response import Response
from rest_framework import viewsets
from delegate_app.api.serializers import DelegateSerializer

class DelegateViewSet(viewsets.ModelViewSet):
    queryset = Delegation.objects.all()
    serializer_class = DelegateSerializer

class DelegateDetail(MainDetail):
	model_type = Delegation
	model_serializer = DelegateSerializer

	def put(self, request, pk, format=None):
		sample = self.get_object(pk)
		old_status = sample.status
		serializer = self.model_serializer(sample, data=request.data)
		if serializer.is_valid():
			serializer.save()
			if old_status is None and request.data['status'] is True:
				print("KEK")
				#do smth to add task with id=pk to owner
			return Response(serializer.data)
		return Response(serializer.errors)
	