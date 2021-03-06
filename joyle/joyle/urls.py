"""joyle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
#from rest_framework import routers
#from main_app import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
	#url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('auth_app.urls')),
    url(r'^api/v1.0/', include('main_app.api.urls')),
    url(r'^api/v1.0/chat/', include('chat_app.api.urls')),
    url(r'^api/v1.0/delegate/', include('delegate_app.api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
