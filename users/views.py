#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from users.models import Client, device
from django.contrib import messages
from users.forms import LoginForm, UserInscriptionForm, GadzEditForm, UserEditForm, MacForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import exceptions
from intra.pattern_decorators import hasrezal_required
# Create your views here.

def loginPage(request):
	if request.user.is_authenticated():
		return redirect(index)
	form = generalLogin(request)	
	if form == None:
		return redirect(index)
	return render(request, "users/login.html")

def generalLogin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data['user']
			password = form.cleaned_data['password']
			user = authenticate(username = user, password = password)
			if user and user.is_active:
				login(request, user)
				messages.success(request, u"Connexion réussie !")
				c = Client.objects.get(pk = user.pk)
				if c.is_gadz and not c.bucque:
					messages.error(request, u"Pense à rajouter ta bucque dans les paramètres de ton compte !")
				return None
			elif user and not user.is_active:
				messages.error(request, u"Votre compte est désactivé, contactez le support")
				return None
			else:
				logout(request)
				messages.error(request, u"Une erreur est survenue lors de la connexion")
				return redirect("users.views.loginPage")
		else:
			messages.error(request, u"Une erreur est survenue lors de la connexion")
			return redirect("users.views.loginPage")
	else:
		form = LoginForm()
	return form

def inscription(request):
	if request.method == 'POST':
		form = UserInscriptionForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.set_password(user.password)
			user.save()
			messages.success(request, u"Création du compte réussie !")
			return redirect("users.views.index")
		else:
			messages.error(request, u"Une erreur est survenue lors de la création du compte")
	else:
		form = UserInscriptionForm()
	return render(request, "users/inscription.html", {'form' : form })


def index(request):
	return render(request, "users/index.html")

@login_required
def settings(request):
	try:
		gadz = Client.objects.get(username = request.user.username)
		a = 0
		if gadz.is_gadz:
			f = GadzEditForm
			a = gadz
		else:
			f = UserEditForm
			a = gadz
	except (AttributeError, exceptions.ObjectDoesNotExist):
		f = UserEditForm
		a = request.user
	if request.method == 'POST':
		form = f(request.POST, instance =a)
		if form.is_valid(): 
			form.save()
			messages.success(request, u"Modification(s) réussie(s)")
			return redirect("users.views.settings")
		else:
			messages.error(request, form.cleaned_data()) 
			messages.error(request, u"Une erreur est survenue lors de la modification")
			return redirect("users.views.settings")
	else:
		form = f(instance = a)
	return render(request, 'users/settings.html', {'form' : form})


def has_rezal_check(user):
	#b = Client.objects.get(pk = user.pk, has_rezal = True)
	b = Client.objects.filter(has_rezal = True)
	c = Client.objects.get(pk = user.pk)
	h = False
	if c in b:
		h = True
	return h

@login_required
@user_passes_test(has_rezal_check)
def add_mac(request):
	if request.method == 'POST':
		form = MacForm(request.POST)
		if form.is_valid():
			form = form.save(commit = False)
			b = Client.objects.get(pk = request.user.pk)
			form.publisher = b
			mac = form.mac
			
			form.save()
			messages.success(request, u"Adresse MAC ajoutée")
			return redirect("users.views.show_mac")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("users.views.show_mac")
	else:
		form = MacForm()
	return render(request, 'users/add_mac.html', {'form' : form})

@login_required
@user_passes_test(has_rezal_check)
def show_mac(request):
	b = Client.objects.get(pk = request.user.pk)
	listmac = device.objects.filter(publisher = b).values_list('nom','mac')
	return render(request, 'users/show_mac.html', {'listmac' : listmac })
