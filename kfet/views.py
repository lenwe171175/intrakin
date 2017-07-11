#-*- coding: utf-8 -*-

from operator import itemgetter
from itertools import chain
from django.shortcuts import render, redirect, HttpResponse
from users.models import Client
from kfet.models import transactionboulc, transactionvp, transactionpg, inputmethod, product, entity, cashinput
from django.db.models import Q
from django.core import exceptions
from users.views import index
from kfet.forms import VirtualtransactionpgForm, transactionpgForm, strpgForm, cashinputForm, VirtualcashinputForm, seuilpgForm, histopgForm, VirtualbucquageboulcForm, bucquageboulcForm, productForm, VirtualproductForm, productEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

import json

# Create your views here.

def is_debucquable_check(user):
	c = Client.objects.get(pk = user.pk)
	h = False
	if c.is_debucquable:
		h = True
	return h

def has_group_can_add_money(user):
	h = False
	if user.groups.filter(name='can_add_money').exists():
		h = True
	return h
	
def has_group_can_create_product(user):
	h = False
	if user.groups.filter(name='can_create_product').exists():
		h = True
	return h

def has_group_can_negats(user):
	h = False
	if user.groups.filter(name='can_negats').exists():
		h = True
	return h

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
			tmp["results"].append({"title": str(i.nom + ' / ' + i.prenom + ' / ' + i.bucque + ' / ' + i.fams)})
		else:
			tmp["results"].append({"title": i.nom + ' / ' + i.prenom})
	return HttpResponse(json.dumps(tmp), content_type = "text/javascript")

def getProducts(request):
	data = []
	grp = request.user.groups.all().values_list('name')
	ent = entity.objects.filter(Q(name__in=grp))
	try:
		field = request.GET.get('prod', '')
		data = product.objects.filter(((Q(name__icontains=field) & Q(associated_entity__in=ent)) | (Q(associated_entity__in=ent) & Q(shortcut__icontains=field))))
	except (KeyError, exceptions.ObjectDoesNotExist, ValueError):
		pass
	tmp = {}
	tmp["results"] = []
	for i in data:
		tmp["results"].append({"title": str(i.name + '  / (' + i.shortcut + ')')})
	return HttpResponse(json.dumps(tmp), content_type = "text/javascript")


@login_required
@user_passes_test(is_debucquable_check)
def addtrpg(request):
	if request.method == 'POST':
		form = transactionpgForm(request.POST)
		if form.is_valid():
			trgt = Client.objects.get(pk = request.user.pk)
			fcd=str(form.cleaned_data['pg']).lower().split(" / ")
			src = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd))
			amnt = form.cleaned_data['amount']
			descrip = form.cleaned_data['description']
			vform = VirtualtransactionpgForm()
			vform = vform.save(commit=False)
			vform.target=src
			vform.source=trgt
			vform.amount=amnt
			vform.description=descrip
			if src != trgt and amnt > 0:
				vform.save()
				messages.success(request, u"Demande effectuée")
				return redirect("kfet.views.summarytrpg")
			else:
				messages.error(request, u"Une erreur est survenue")
				return redirect("kfet.views.addtrpg")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("kfet.views.addtrpg")
	else:
		form=transactionpgForm()
	return render(request, "kfet/addtrpg.html")
	
@login_required	
@user_passes_test(is_debucquable_check)	
def summarytrpg(request):
	b = Client.objects.get(pk = request.user.pk)
	listtrpgdone = transactionpg.objects.filter(Q(source = b) & Q(accepted = 0)).values_list('target__nom','amount','description','date')
	listtrpgtodo = transactionpg.objects.filter(Q(target = b) & Q(accepted = 0)).values_list('source__nom', 'amount', 'description')
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

@login_required
@user_passes_test(has_group_can_add_money)
def cashinputview(request):
	if request.method == 'POST':
		form = cashinputForm(request.POST)
		print form
		if form.is_valid():
			authorci=Client.objects.get(pk = request.user.pk)
			fcd=str(form.cleaned_data['pg']).lower().split(" / ")
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
				return redirect("kfet.views.cashinputview")
			else:
				messages.warning(request, u"Le montant doit etre positif !")
				return redirect("kfet.views.cashinputview")
		else:
			messages.error(request, u"Une erreur est survenue")
			return redirect("kfet.views.cashinputview")
	else:
		form = cashinputForm()
	return render(request, "kfet/cashinput.html", {'form' : form})

@login_required
@user_passes_test(has_group_can_negats)
def seuilpg(request):
	if request.method == 'POST':
		form = seuilpgForm(request.POST)
		if form.is_valid():
			montant = form.cleaned_data['seuil']
			if str(form.cleaned_data['proms']) != "...":
				promos = str(form.cleaned_data['proms']).lower().split(";")
				for elt in promos:
					if not elt.isdigit():
						messages.error(request, u"Mauvaise saisie des prom's")
						return render(request, "kfet/seuilpg.html")
				listmatch = []
				for i in range(len(promos)):
					listmatch += Client.objects.filter(Q(credit__lt=montant) & Q(proms = promos[i])).values_list('nom','prenom','proms','credit')
			else:
				listmatch = Client.objects.filter(Q(credit__lt=montant)).values_list('nom','prenom','proms','credit')
			if len(listmatch) == 0:
				messages.error(request, u"Aucun PG ne correspond")
				return render(request, "kfet/seuilpg.html")
			else:
				print(listmatch)
				return render(request, "kfet/seuilpg.html", {'listmatch' : listmatch})
		else:
			messages.error(request, u"Une erreur est survenue")
			return render(request, "kfet/seuilpg.html")
	else:
		form = seuilpgForm()
	return render(request, "kfet/seuilpg.html")
	
@login_required
def histopg(request):
	if request.method == 'POST':
		form = histopgForm(request.POST)
		if form.is_valid():
			fcd=str(form.cleaned_data['pg']).lower().split(" / ")
			pkpg = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd)).pk
			bucquepg = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd)).bucque
			if len(fcd) == 0:
				messages.error(request, u"Aucun PG ne correspond")
				return render(request, "kfet/histopg.html")
		else:
			messages.error(request, u"Une erreur est survenue")
			return render(request, "kfet/histopg.html")
	else:
		form = histopgForm()
		pkpg = Client.objects.filter(Q(pk = request.user.pk)).values_list('pk')
		bucquepg = Client.objects.filter(Q(pk = request.user.pk)).values_list('bucque')

	tpg_list=transactionpg.objects.filter(Q(target = pkpg) | Q(source = pkpg))
	tbc_list=transactionboulc.objects.filter(Q(target = pkpg))
	tvp_list=transactionvp.objects.filter(Q(target = pkpg))
	tci_list=cashinput.objects.filter(Q(target = pkpg))
	
	query_result = sorted(chain(tpg_list, tbc_list, tvp_list, tci_list), key=lambda instance: instance.date, reverse=True)
	listmatch = []
	for result in query_result:
		inter_listmatch=[]
		if result.__class__.__name__ == "transactionpg":
			current_result = result
			bucque_field = getattr(getattr(current_result, 'source'),'bucque')
			target_bucque_field = getattr(getattr(current_result, 'target'),'bucque')
			inter_listmatch.extend([bucque_field, getattr(current_result,'amount'),getattr(current_result, 'description'),getattr(current_result, 'date'),target_bucque_field, "trpg"])
		elif result.__class__.__name__ == "transactionboulc":
			current_result = result
			bucque_field = getattr(current_result, 'entite')
			authortb_field = getattr(getattr(current_result, 'authortb'),'bucque')
			inter_listmatch.extend([bucque_field, getattr(current_result, 'product_price'), getattr(current_result, 'product_name'), getattr(current_result, 'date'), authortb_field, "trb"])
		elif result.__class__.__name__ == "transactionvp":
			current_result = result
			bucque_field = getattr(current_result, 'entite')
			inter_listmatch.extend([bucque_field, getattr(current_result, 'product_price'), getattr(current_result, 'product_name'), getattr(current_result, 'date'), getattr(current_result, 'authortvp'), "trvp"])
		elif result.__class__.__name__ == "cashinput":
			current_result = result
			bucque_field = getattr(getattr(current_result, 'target'), 'bucque')
			authorci_field = getattr(getattr(current_result, 'authorci'),'bucque')
			inter_listmatch.extend([bucque_field, getattr(current_result, 'amount'), getattr(current_result, 'method'), getattr(current_result, 'date'), authorci_field, "ci"])
		listmatch.append(inter_listmatch)
		
	return render(request, "kfet/histopg.html", {'listmatch' : listmatch, 'bucquepg' : bucquepg[0][0]})

@login_required
@user_passes_test(has_group_can_create_product)
def bucquageboulc(request):
	if request.method== 'POST':
		form  = bucquageboulcForm(request.POST)
		if form.is_valid():
			authortb=Client.objects.get(pk = request.user.pk)
			fcd=str(form.cleaned_data['pg']).lower().split(" / ")
			target = Client.objects.get(Q(nom__in=fcd) & Q(prenom__in=fcd))
			product_to_search=str(form.cleaned_data['prod']).lower().split(" / ")
			product_to_apply=product.objects.get(Q(name__in=product_to_search))
			product_price=product_to_apply.price
			product_name=product_to_apply.name
			entite=product_to_apply.associated_entity
			target_credit = target.credit
			if request.user.groups.filter(name='can_negats').exists() or target_credit >= product_price:
				vform = VirtualbucquageboulcForm()
				vform = vform.save(commit=False)
				vform.authortb=authortb
				vform.target=target
				vform.product_price=product_price
				vform.product_name=product_name
				vform.entite=entite
				vform.save()
				Client.debitpg(target,product_price)
				messages.success(request, u"Bucquage effectué")
				return render(request, "kfet/bucquageboulc.html")
			else:
				messages.error(request, u"Pas assez d'argent sur le compte cible")
				return render(request, "kfet/bucquageboulc.html")
		else:
			messages.error(request, u"Une erreur est survenue")
			return render(request, "kfet/bucquageboulc.html")
		return render(request, "kfet/bucquageboulc.html")
	
	else:
		form=bucquageboulcForm()
	return render(request, "kfet/bucquageboulc.html")
	
@login_required
@user_passes_test(has_group_can_create_product)
def productcreation(request):
	if request.method == 'POST':
		form = productForm(request.POST)
		print form
		if form.is_valid():
			name = form.cleaned_data['name']
			price = form.cleaned_data['price']
			entityvalue = form.cleaned_data['entity']
			shortcut = form.cleaned_data['shortcut']
			if request.user.groups.filter(name=entityvalue.lower()).exists():
				vform = VirtualproductForm()
				vform = vform.save(commit=False)
				vform.name = name
				vform.price = price
				vform.shortcut = shortcut
				vform.associated_entity=entity.objects.get(name = entityvalue.lower())
				vform.save()
				messages.success(request, u"Création réussie")
				return render(request, "kfet/productcreation.html")
			else:
				form = productForm()
				messages.error(request, u"Impossible de créer le produit pour l'entité sélectionnée")
				return render(request, "kfet/productcreation.html")
		else:
			messages.error(request, u"Une erreur est survenue")
			return render(request, "kfet/productcreation.html")
	else:
		form = productForm()
	return render(request, "kfet/productcreation.html")
	
@login_required
@user_passes_test(has_group_can_create_product)
def productdisplay(request):
	current_user_group = request.user.groups.all().values_list('name')
	user_entity = entity.objects.filter(Q(name__in=current_user_group))
	list_existing_product = product.objects.filter(Q(associated_entity__in=user_entity)).values_list('name','price','shortcut')
	if request.method == 'POST':
		if request.POST.__contains__('edit_product'):
			req_nbr = request.POST.__getitem__('edit_product')
			instance_to_pass = product.objects.filter(Q(associated_entity__in=user_entity))[int(req_nbr)]
			return redirect("kfet.views.productedit", id_product = instance_to_pass.pk)
		elif request.POST.__contains__('delete_product'):
			req_nbr = request.POST.__getitem__('delete_product')
			instance_to_pass = product.objects.filter(Q(associated_entity__in=user_entity))[int(req_nbr)]
			if getattr(instance_to_pass, 'name') == list_existing_product[int(req_nbr)][0]:
				instance_to_pass.delete()
				messages.success(request, u"Suppression réussie !")
				return redirect("kfet.views.productdisplay")
			else:
				messages.error(request, u"Une erreur est survenue")
				return redirect("kfet.views.productdisplay")
	return render(request, "kfet/productdisplay.html", {'listproduct' : list_existing_product})

@login_required
@user_passes_test(has_group_can_create_product)
def productedit(request, id_product):
	object_to_manage = product.objects.get(pk=id_product)
	if request.method == 'POST':
		form = productEditForm(request.POST, instance = object_to_manage)
		if form.is_valid():
			form.save()
			messages.success(request, u"Modification réussie !")
			return redirect("kfet.views.productdisplay")
		else:
			messages.success(request, u"Une erreur est survenue")
			return redirect("kfet.views.productdisplay")
	else:
		form = productEditForm(instance = object_to_manage)
	return render(request, "kfet/productedit.html", {'form' : form, 'instance' : object_to_manage.pk})			
			
			
			
			
			
			
			
			
			
			
			
			
	