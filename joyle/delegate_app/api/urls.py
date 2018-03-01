from django.conf.urls import url, include
from main_app.api import views
from delegate_app.api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.DelegateViewSet)

urlpatterns = [
	url(r'^(?P<pk>[0-9]*)$', views.DelegateDetail.as_view()),
	url(r'^list', include(router.urls)),
]