#-*- coding: utf-8 -*-
from django import forms
from kfet.models import transactionpg

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
		
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(strpgForm, self).__init__(*args, **kwargs)
