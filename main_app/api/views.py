from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from main_app.models import Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MainDetail(APIView):

	permission_classes = (IsAuthenticated,)

	model_type = object
	model_serializer = object 

	def get_object(self, pk):
		try:
			return self.model_type.objects.get(pk=pk)
		except self.model_type.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		if pk:
			sample = self.get_object(pk)
			serializer = self.model_serializer(sample)
		else:
			samples = self.model_type.objects.all()
			serializer = self.model_serializer(samples, many=True)
		return Response(serializer.data)
	
	def post(self, request, pk, format=None):
		serializer = self.model_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	def put(self, request, pk, format=None):
		sample = self.get_object(pk)
		serializer = self.model_serializer(sample, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	def delete(self, request, pk, format=None):
		sample = self.get_object(pk)
		sample.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class TaskDetail(MainDetail):
	model_type = Task
	model_serializer = TaskSerializer

class ProjectDetail(MainDetail):
	model_type = Project
	model_serializer = ProjectSerializer
