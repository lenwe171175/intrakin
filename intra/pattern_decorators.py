from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.core import exceptions
from users.models import Client
from django.contrib import messages

def hasrezal_required(function):
	@login_required
	def modified_function(request, *args, **kwargs):
		try:
			gadz = Client.objects.get(username = request.user.username)
			if not gadz.has_rezal:
				messages.error(request, u"Vous n'avez pas l'autorisation de faire cette action")
				return redirect("users.views.index")
		except (AttributeError, exceptions.ObjectDoesNotExist):
			messages.error(request, u"Une erreur est survenue")
			return redirect("users.views.index")
		return function(request, *args, **kwargs)
	return modified_function
