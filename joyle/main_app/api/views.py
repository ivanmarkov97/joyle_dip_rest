from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from main_app.models import (Project,
							 Task,
							 ProjectGroup,
							 Relation)
from .serializers import (ProjectSerializer, 
						  TaskSerializer,
						  UserSerializer,
						  ProjectGroupSerializer,
						  RelationSerializer)
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

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectGroupViewSet(viewsets.ModelViewSet):
    queryset = ProjectGroup.objects.all()
    serializer_class = ProjectSerializer

class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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
			print(request.user)
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


class ProjectDetail(MainDetail):
	model_type = Project
	model_serializer = ProjectSerializer

class ProjectGroupDetail(MainDetail):
	model_type = ProjectGroup
	model_serializer = ProjectGroupSerializer

	def post(self, request, pk, format=None):
		data = request.data
		cr_id = int(data['owner'])
		prj_id = int(data['project'])
		prj = Project.objects.get(pk=prj_id)
		if cr_id == prj.owner.id:
			data_ok = {}
			data_ok['name'] = data['name']
			data_ok['project'] = data['project']
			serializer = self.model_serializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
		return Response({"detail": "You can't create group for this project. You're not owner"})

class RelationDetail(MainDetail):
	model_type = Relation
	model_serializer = RelationSerializer

class TaskDetail(MainDetail):
	model_type = Task
	model_serializer = TaskSerializer

	def delete(self, request, pk, format=None):
		task = self.get_object(pk)
		task.is_deleted = True
		task.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

