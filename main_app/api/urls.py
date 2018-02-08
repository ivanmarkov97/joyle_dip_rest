from django.conf.urls import url, include
from main_app.api import views
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
#router.register(r'projects', views.ProjectViewSet)
#router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
	url(r'^auth/token', obtain_jwt_token),
	url(r'^tasks/(?P<pk>[0-9]*)$', views.TaskDetail.as_view()),
	url(r'^projects/(?P<pk>[0-9]*)$', views.ProjectDetail.as_view()),
	url(r'^', include(router.urls)),
]