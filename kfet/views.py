#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse
from users.models import Client
from kfet.models import transactionpg, inputmethod
from django.db.models import Q
from django.core import exceptions
from users.views import index
from kfet.forms import VirtualtransactionpgForm, transactionpgForm, strpgForm, cashinputForm, VirtualcashinputForm
from django.contrib import messages

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

def addtrpg(request):
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
			vform.target=src
			vform.source=trgt
			vform.amount=amnt
			vform.description=descrip
			if src != trgt and amnt > 0 and amnt <= trgt.credit:
				vform.save()
				messages.success(request, u"Demande effectuée")
				return redirect("kfet.views.summarytrpg")
			else:
				if amnt > trgt.credit:
					messages.warning(request,u"Tu n'as pas assez d'argent !")
				messages.error(request, u"Une erreur est survenue")
				return redirect("kfet.views.addtrpg")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("kfet.views.addtrpg")
	else:
		form=transactionpgForm()
	return render(request, "kfet/addtrpg.html")
			
def summarytrpg(request):
	b = Client.objects.get(pk = request.user.pk)
	listtrpgdone = transactionpg.objects.filter(Q(source = b) & Q(accepted = 0)).values_list('target','amount','description','date')
	listtrpgtodo = transactionpg.objects.filter(Q(target = b) & Q(accepted = 0)).values_list('source', 'amount', 'description')
	if request.method == 'POST':
		req = request.POST.__getitem__('idnbr')
		trpgtodo = transactionpg.objects.filter(Q(target = b) & Q(accepted = 0))
		formfilling = trpgtodo[int(req)]
		form = strpgForm(instance=formfilling)
		form = form.save(commit = False)
		if b.credit >= form.amount:
			form.accepted = 1
			form.save()
			Client.debitpg(b, form.amount)
			Client.creditpg(form.source, form.amount)
			messages.success(request, u"Transaction effectuée")
			return redirect("kfet.views.summarytrpg")
		else:
			messages.warning(request, u"Tu n'as pas assez d'argent !")
			return redirect("kfet.views.summarytrpg")
	return render(request, "kfet/strpg.html", {'donelist' : listtrpgdone, 'todolist' : listtrpgtodo})

def cashinput(request):
	if request.method == 'POST':
		form = cashinputForm(request.POST)
		print form
		if form.is_valid():
			authorci=Client.objects.get(pk = request.user.pk)
			fcd=str(form.cleaned_data['pg']).lower().split(" ")
			trgt = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd))
			amnt = form.cleaned_data['amount']
			im=inputmethod.objects.get(name = form.cleaned_data['method'])
			print im
			vform = VirtualcashinputForm()
			vform = vform.save(commit=False)
			vform.authorci=authorci
			vform.target=trgt
			vform.amount=amnt
			vform.method=im
			if amnt > 0:
				vform.save()
				Client.creditpg(trgt,amnt)
				messages.success(request, u"Ajout effectué !")
				return redirect("kfet.views.cashinput")
			else:
				messages.warning(request, u"Le montant doit etre positif !")
				return redirect("kfet.views.cashinput")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("kfet.views.cashinput")
	else:
		form = cashinputForm()
	return render(request, "kfet/cashinput.html", {'form' : form})
