# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.

class CustomObtainAuthToken(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
		token = Token.objects.get(key=response.data['token'])
		return Response({'token': token.key, 'id': token.user_id})


class AuthView(APIView):

	#authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):
		content = {
			'user': unicode(request.user),  # `django.contrib.auth.User` instance.
			'auth': unicode(request.auth),  # None
 		}
 		return Response(content)
