#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import exceptions
from users.models import Client

# Create your models here.

class transactionvp(models.Model):
	authortvp=models.CharField(max_length=200, default="VP")
	target=models.ForeignKey('users.Client', related_name='transactionvp_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	product_price=models.DecimalField(max_digits=5, decimal_places=2)
	product_name=models.CharField(max_length=200)
	accepted=models.BooleanField(default=True)
	entite=models.CharField(max_length=200, default='Kfet')

	def __unicode__(self):
		return self.product_name

class transactionboulc(models.Model):
	authortb=models.ForeignKey('users.Client', related_name='transactionboulc_authortb')
	target=models.ForeignKey('users.Client', related_name='transactionboulc_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	product_price=models.DecimalField(max_digits=5, decimal_places=2)
	product_name=models.CharField(max_length=200)
	accepted=models.BooleanField(default=True)
	entite=models.CharField(max_length=200, default='Kfet')

	def __unicode__(self):
		return self.product_name

class transactionpg(models.Model):
	source=models.ForeignKey('users.Client', related_name='transactionpg_source')
	target=models.ForeignKey('users.Client', related_name='transactionpg_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	amount=models.DecimalField(max_digits=5, decimal_places=2)
	description=models.CharField(max_length=200)
	accepted=models.BooleanField(default=False)

	def __unicode__(self):
		return self.description

class cashinput(models.Model):
	authorci=models.ForeignKey('users.Client', related_name='cashinput_authorci')
	target=models.ForeignKey('users.Client', related_name='cashinput_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	amount=models.DecimalField(max_digits=5, decimal_places=2)
	method=models.ForeignKey('inputmethod')

class inputmethod(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class product(models.Model):
	name=models.CharField(max_length=200)
	price=models.DecimalField(max_digits=5, decimal_places=2)
	associated_entity=models.ForeignKey('entity')
	shortcut=models.CharField(max_length=5, unique=True)
	instant=models.BooleanField(default=1)

	def __unicode__(self):
		return self.name

class entity(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
	

