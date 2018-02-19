from django.conf.urls import url, include
from main_app.api import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
#router.register(r'projects', views.ProjectViewSet)
#router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
	url(r'^tasks/(?P<pk>[0-9]*)$', views.TaskDetail.as_view()),
	url(r'^projects/(?P<pk>[0-9]*)$', views.ProjectDetail.as_view()),
	url(r'^project_groups/(?P<pk>[0-9]*)$', views.ProjectGroupDetail.as_view()),
	url(r'^relations/(?P<pk>[0-9]*)$', views.RelationDetail.as_view()),
	url(r'^', include(router.urls)),
]