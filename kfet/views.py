#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse
from users.models import Client
from kfet.models import transactionpg
from django.db.models import Q
from django.core import exceptions
from users.views import index
from kfet.forms import VirtualtransactionpgForm, transactionpgForm
from django.contrib import messages
from kfet.models import transactionpg

import json


# Create your views here.

def getPgs(request):
	data = []
	try:
		pg = request.GET.get('pg', '')
		data = Client.objects.filter((Q(bucque__icontains=pg) | Q(nom__icontains=pg)) & Q(is_debucquable=1))
	except (KeyError, exceptions.ObjectDoesNotExist, ValueError):
		pass
	tmp = {}
	tmp["results"] = []
	for i in data:
		if i.bucque:
			tmp["results"].append({"title": str(i.nom + ' ' + i.prenom + ' ou ' + i.bucque + ' ' + i.fams)})
		else:
			tmp["results"].append({"title": i.nom + ' ' + i.prenom})
	return HttpResponse(json.dumps(tmp), content_type = "text/javascript")

def transactionpg(request):
	if request.method == 'POST':
		form = transactionpgForm(request.POST)
		if form.is_valid():
			trgt = Client.objects.get(pk = request.user.pk)
			fcd=str(form.cleaned_data['pg']).lower().split(" ")
			src = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd))
			amnt = form.cleaned_data['amount']
			descrip = form.cleaned_data['description']
			vform = VirtualtransactionpgForm()
			vform = vform.save(commit=False)
			vform.target=trgt
			vform.source=src
			vform.amount=amnt
			vform.description=descrip
			if src != trgt and amnt > 0:
				vform.save()
				messages.success(request, u"Demande effectuée")
				return redirect("kfet.views.transactionpg")
			else:
				messages.error(request, u"Une erreur est survenue")
				return redirect("kfet.views.transactionpg")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("kfet.views.transactionpg")
	else:
		form=transactionpgForm()
	return render(request, "kfet/transactionpg.html")
			
