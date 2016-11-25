# coding: utf-8
from users.models import Client
from django.core import exceptions
from django.contrib import messages

def getGadz(request):
	try:
		gadz = Client.objects.get(username = request.user.username)
	except (AttributeError, exceptions.ObjectDoesNotExist):
		gadz = None
	return {'gadz' : gadz}
