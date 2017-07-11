#-*- coding: utf-8 -*-
from django import forms
from kfet.models import transactionpg, cashinput, transactionboulc, product

class transactionpgForm(forms.Form):
	pg = forms.CharField()
	amount = forms.DecimalField()
	description = forms.CharField()

class VirtualtransactionpgForm(forms.ModelForm):
	class Meta:
		model = transactionpg
		fields = ['source','target','amount','description']
		
class strpgForm(forms.ModelForm):
	class Meta:
		model = transactionpg
		fields = ['source', 'amount', 'description']

class cashinputForm(forms.Form):
	CHOICES = (('CB','CB'),('Espèces','Espèces'),('Chèque','Chèque'),)
	pg = forms.CharField()
	amount = forms.DecimalField()
	method = forms.CharField()

class VirtualcashinputForm(forms.ModelForm):
	class Meta:
		model = cashinput
		fields = ['authorci','target','amount','method']
		
class seuilpgForm(forms.Form):
	seuil = forms.DecimalField()
	proms = forms.CharField()

class histopgForm(forms.Form):
	pg = forms.CharField()
	
class bucquageboulcForm(forms.Form):
	pg = forms.CharField()
	prod = forms.CharField()
	
class VirtualbucquageboulcForm(forms.ModelForm):
	class Meta:
		model = transactionboulc
		fields = ['authortb', 'target','product_price','product_name','entite']
		
class VirtualproductForm(forms.ModelForm):
	class Meta:
		model = product
		fields = ['name','price','associated_entity','shortcut']
		
class productForm(forms.Form):
	CHOICES = (('Kfet','Kfet'),('Cvis','Cvis'),('Kve','Kve'),)
	name = forms.CharField()
	price = forms.DecimalField()
	entity = forms.CharField()
	shortcut = forms.CharField()
	
class productEditForm(forms.ModelForm):
	class Meta:
		model = product
		fields = ['name','price','shortcut']
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(productEditForm, self).__init__(*args, **kwargs)