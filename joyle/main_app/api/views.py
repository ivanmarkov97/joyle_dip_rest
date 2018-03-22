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

class AllDetail(APIView):
	permission_classes = (IsAuthenticated,)

	def get(self, request, pk, format=None):
		if pk:
			all_user_projects = Project.objects.all().filter(owner=pk)
			all_user_tasks = Task.objects.all().filter(owner=pk)
			all_user_project_groups = ProjectGroup.objects.all().filter(owner=pk)
			all_user_relations = Relation.objects.all().filter(owner=pk)

			content = {}

			project_serializer = ProjectSerializer(all_user_projects, many=True)
			task_serializer = TaskSerializer(all_user_tasks, many=True)
			project_group_serializer = ProjectGroupSerializer(all_user_project_groups, many=True)
			relation_serializer = RelationSerializer(all_user_relations, many=True)

			content['user'] = pk
			content['projects'] = project_serializer.data
			content['tasks'] = task_serializer.data
			content['project_groups'] = project_group_serializer.data
			content['relations'] = relation_serializer.data

			return Response(content)
		else:
			return Response({"detail": "permition denied"}) 


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

	def post(self, request, pk, format=None):
		p_pos = len(Project.objects.all())
		valid_data = request.data
		valid_data['position'] = p_pos
		serializer = self.model_serializer(data=valid_data)
		if serializer.is_valid():
			serializer.save()
			print(request.user)
			cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
			return Response(serializer.data)
		return Response(serializer.errors)

	def delete(self, request, pk, format=None):
		project = self.get_object(pk)
		replace_projects = Project.objects.all().filter(owner=request.data['owner']).filter(position__gte=project.position)
		if replace_projects:
			for prj in replace_projects:
				prj.position = prj.position - 1
				prj.save()
		project.delete()
		cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
		return Response(status=status.HTTP_204_NO_CONTENT)


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
	cache_model_name = "relations"

class TaskDetail(MainDetail):
	model_type = Task
	model_serializer = TaskSerializer
	cache_model_name = "tasks"

	def post(self, request, pk, format=None):
		valid_data = request.data
		if not request.data['parent']:
			t_pos = len(Task.objects.all() \
									.filter(owner=request.data['owner']) \
									.filter(project=request.data['project']).filter(parent=None)
						)
			valid_data['position'] = p_pos
		serializer = self.model_serializer(data=valid_data)
		if serializer.is_valid():
			serializer.save()
			print(request.user)
			cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
			return Response(serializer.data)
		return Response(serializer.errors)

	def put(self, request, pk, format=None):
		if pk:
			task = self.get_object(int(request.data['id']))
			old_pos = task.position
			old_parent = task.parent
			new_pos = request.data['position']
			new_parent = request.data['parent']
			if old_parent != new_parent:
				print("I am here")
				replace_old_tasks = self.model_type.objects.all() \
													.filter(owner=request.data['owner']) \
													.filter(parent=old_parent) \
													.filter(position__gt=old_pos)
				if replace_old_tasks:
					for rep_task in replace_old_tasks:
						rep_task.position = rep_task.position - 1
						rep_task.save()

				replace_new_tasks = self.model_type.objects.all() \
													.filter(owner=request.data['owner']) \
													.filter(parent=new_parent) \
													.filter(position__gte=new_pos)
				if replace_new_tasks:
					for rep_task in replace_new_tasks:
						rep_task.position = rep_task.position + 1
						rep_task.save()
				task_serializer = TaskSerializer(task, data=request.data)
				if task_serializer.is_valid():
					task_serializer.save()
					return Response(task_serializer.data)
				return Response(task_serializer.errors)

			elif new_pos != old_pos:
				print("I am here 2")
				if new_pos > old_pos:
					replace_tasks = self.model_type.objects.all() \
													.filter(owner=request.data['owner']) \
													.filter(parent=request.data['parent']) \
													.filter(position__gt=old_pos) \
													.filter(position__lte=new_pos)
					if replace_tasks:
						for rep_task in replace_tasks:
							rep_task.position = rep_task.position - 1
							rep_task.save()
				if new_pos < old_pos:
					replace_tasks = self.model_type.objects.all() \
													.filter(owner=request.data['owner']) \
													.filter(parent=request.data['parent']) \
													.filter(position__lt=old_pos) \
													.filter(position__gte=new_pos)
					if replace_tasks:
						for rep_task in replace_tasks:
							rep_task.position = rep_task.position + 1
							rep_task.save()
				task_serializer = TaskSerializer(task, data=request.data)
				if task_serializer.is_valid():
					task_serializer.save()
					return Response(task_serializer.data)
				return Response(task_serializer.errors)
			else:
				print("I am here 3")
				task_serializer = TaskSerializer(task, data=request.data)
				if task_serializer.is_valid():
					task_serializer.save()
					cache.delete(self.cache_model_name + '_user_' + str(request.data['owner']))
					return Response(task_serializer.data)
				return Response(task_serializer.errors)

		else:
			print("I am here 4")
			serializer = self.model_serializer(data=request.data, many=True)
			if serializer.is_valid():
				print(serializer.data)
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors)
