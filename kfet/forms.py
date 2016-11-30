#-*- coding: utf-8 -*-
from django import forms
from kfet.models import transactionpg, cashinput

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
