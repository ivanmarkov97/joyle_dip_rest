from django.conf.urls import url, include
from chat_app.api import views

urlpatterns = [
	url(r'^$', views.MessageViewSet),
	url(r'^messages/(?P<pk>[0-9]*)$', views.MessageDetail.as_view()),
]
