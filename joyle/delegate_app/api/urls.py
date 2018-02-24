from django.conf.urls import url
from main_app.api import views
from delegate_app.api import views
#from rest_framework import routers

"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'project_groups', views.ProjectGroupViewSet)
router.register(r'relations', views.RelationViewSet)
"""

urlpatterns = [
	url(r'^send/(?P<pk>[0-9]*)$', views.DelegateDetail.as_view()),
	#url(r'^', include(router.urls)),
]