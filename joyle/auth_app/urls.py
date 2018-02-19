from django.conf.urls import url, include
#from rest_framework_jwt.views import obtain_jwt_token
from auth_app import views

urlpatterns = [
	url(r'^$', views.AuthView.as_view()),
	url(r'^token$', views.CustomObtainAuthToken.as_view()),
]
