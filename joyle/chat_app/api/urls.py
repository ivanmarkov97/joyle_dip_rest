from django.conf.urls import url, include
from chat_app.api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.MessageViewSet)

urlpatterns = [
	url(r'^messages/(?P<pk>[0-9]*)$', views.MessageDetail.as_view()),
	url(r'^list', include(router.urls)),
]
