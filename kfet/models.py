#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import exceptions
from users.models import Client

# Create your models here.

class account(models.Model):
	name = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
	fams = models.CharField(blank=True, max_length=200, verbose_name = u"Fam's")
	bucque = models.CharField(blank=True, max_length=200)
	proms = models.CharField(blank=True, max_length=200, verbose_name = u"Prom's")
	credit = models.DecimalField(max_digits = 5, decimal_places = 2)
	date_negatss = models.DateTimeField(blank=True, null=True)
	is_debucquable=models.BooleanField(default=False)
	associated=models.ForeignKey('users.Client', blank=True, null=True)

	def __unicode__(self):
		return self.name

class transactionentity(models.Model):
	source=models.ForeignKey('account', related_name='transactionentity_source')
	target=models.ForeignKey('account', related_name='transactionentity_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	product_price=models.DecimalField(max_digits=5, decimal_places=2)
	product_name=models.CharField(max_length=200)
	accepted=models.BooleanField(default=True)

	def __unicode__(self):
		return self.product_name

class transactionpg(models.Model):
	source=models.ForeignKey('account', related_name='transactionpg_source')
	target=models.ForeignKey('account', related_name='transactionpg_target')
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	amount=models.DecimalField(max_digits=5, decimal_places=2)
	description=models.CharField(max_length=200)
	accepted=models.BooleanField(default=False)

	def __unicode__(self):
		return self.description

class cashinput(models.Model):
	source=models.ForeignKey('account', related_name='cashinput_source')
	target=models.ForeignKey('account', related_name='cashinput_target')
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

	def __unicode__(sefl):
		return self.name

class entity(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
	

