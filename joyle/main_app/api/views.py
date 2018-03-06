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
from django.core.cache import cache

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
	cache_model_name = ""
 
	def get_object(self, pk):
		try:
			return self.model_type.objects.get(pk=pk)
		except self.model_type.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		if request.GET.get('user'):
			usr_id = int(request.GET.get('user'))
			if self.cache_model_name != "":
				if cache.has_key(self.cache_model_name + '_user_' + str(usr_id)):
					print("return cache")
					return Response(cache.get(self.cache_model_name + '_user_' + str(usr_id)))
				else:
					usr = User.objects.get(pk=usr_id)
					samples = self.model_type.objects.all().filter(owner=usr)
					serializer = self.model_serializer(samples, many=True)
					cache.set(self.cache_model_name + '_user_' + str(usr_id), serializer.data, 60)
					return Response(serializer.data)
			else:
				usr = User.objects.get(pk=usr_id)
				samples = self.model_type.objects.all().filter(owner=usr)
				serializer = self.model_serializer(samples, many=True)
				return Response(serializer.data)
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
			cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
			return Response(serializer.data)
		return Response(serializer.errors)

	def put(self, request, pk, format=None):
		sample = self.get_object(pk)
		serializer = self.model_serializer(sample, data=request.data)
		if serializer.is_valid():
			serializer.save()
			cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
			return Response(serializer.data)
		return Response(serializer.errors)

	def delete(self, request, pk, format=None):
		sample = self.get_object(pk)
		sample.delete()
		cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
		return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetail(MainDetail):
	model_type = Project
	model_serializer = ProjectSerializer
	cache_model_name = "projects"

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
		return Response({"detailpy": "You can't create group for this project. You're not owner"})

class RelationDetail(MainDetail):
	model_type = Relation
	model_serializer = RelationSerializer
	cache_model_name = "relations"

class TaskDetail(MainDetail):
	model_type = Task
	model_serializer = TaskSerializer
	cache_model_name = "tasks"

	def put(self, request, pk, format=None):
		serializer = self.model_serializer(data=request.data, many=True)
		if serializer.is_valid():
			print serializer.data
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)