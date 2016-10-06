#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from users.models import Client, device

class LoginForm(forms.Form):
	user = forms.CharField()
	password = forms.CharField()

class UserInscriptionForm(forms.ModelForm):
	password_validation = forms.CharField(required = True, label = u"Entrez de nouveau votre mot de passe", widget = forms.PasswordInput())
	class Meta:
		model = Client
		fields = ['username','nom','prenom','chambre','phone','mail','password']

	def __init__(self, *args, **kwargs):
		super(UserInscriptionForm, self).__init__(*args,**kwargs)
		self.fields['nom'].required = True
		self.fields['prenom'].required = True
		self.fields['chambre'].required = True
		self.fields['phone'].required = True
		self.fields['mail'].required = True
		self.fields['password'].widget = forms.PasswordInput()

	def clean(self):
		cleaned_data = super(UserInscriptionForm, self).clean()
		pass1 = cleaned_data.get('password')
		pass2 = cleaned_data.get('password_validation')
		if pass1 != None and pass1 != pass2:
			raise forms.ValidationError("Erreur : les mots de passe ne correspondent pas")
		return cleaned_data

class UserEditForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['chambre','phone','mail']

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(UserEditForm, self).__init__(*args, **kwargs)
		self.fields['chambre'].required = True
		self.fields['phone'].required = True
		self.fields['mail'].required = True

class GadzEditForm(forms.ModelForm):
	class Meta:
		model = Client
		fields = ['chambre','phone','mail','bucque','fams','proms']

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(GadzEditForm, self).__init__(*args, **kwargs)
		self.fields['chambre'].required = True
		self.fields['phone'].required = True
		self.fields['mail'].required = True

class MacForm(forms.ModelForm):
	class Meta:
		model = device
		exclude = ["publisher"]
	
	#def __init__(self, user, *args, **kwargs):
	#	self.publisher = user
	#	super(MacForm, self).__init__(*args, **kwargs)
