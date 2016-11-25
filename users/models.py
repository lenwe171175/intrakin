#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core import exceptions

import hashlib
import base64
import os

# Create your models here.

class   radreply(models.Model):
	username = models.CharField(max_length = 17)
	attribute = models.CharField(max_length = 254, default = 'WISPR-Bandwidth-Max-Down')
	op = models.CharField(max_length = 2, default = '=')
	value = models.CharField(max_length = 254, default = '960000')

	class Meta:
		db_table = 'radreply'

class   radcheck(models.Model):
	username = models.CharField(max_length = 17)
	attribute = models.CharField(max_length = 64, default = 'Auth-Type')
	op = models.CharField(max_length = 2, default = ':=')
	value = models.CharField(max_length = 64, default = 'Accept')

	class Meta:
		db_table = 'radcheck'

class Client(User):
	nom = models.CharField(max_length = 64)
	prenom = models.CharField(max_length = 64)
	chambre = models.CharField(max_length = 5)
	mail = models.EmailField(max_length = 254)
	phone = models.CharField(max_length = 10)
	bucque = models.CharField(blank = True, max_length = 254)
	fams = models.CharField(blank = True, max_length = 254, verbose_name = u"Fam's")
	proms = models.CharField(blank = True, max_length = 254, verbose_name = u"Prom's")
	has_rezal = models.BooleanField(default = False)
	is_gadz = models.BooleanField(default = False)
	is_conscrit = models.BooleanField(default = False)
	is_debucquable = models.BooleanField(default = False)
	credit = models.DecimalField(max_digits=5, decimal_places=2, default = 0, blank = True)

	def save(self, *args, **kwargs):
		super(Client, self).save(*args, **kwargs)
		b = device.objects.filter(publisher = self.pk)
		if b != []:
			if not self.has_rezal:
				for i in b:
					try:
						tmp = radcheck.objects.filter(username = i.mac)
						tmp.all().delete()
						tmp = radreply.objects.filter(username = i.mac)
						tmp.all().delete()
						i.delete()
					except (exceptions.ObjectDoesNotExist):
						return
		if not self.is_conscrit:
			for i in b:
				try:
					tmp = radreply.objects.filter(username = i.mac)
					tmp.all().delete()
				except (exceptions.ObjectDoesNotExist):
					return

		if self.is_conscrit:
			for i in b:
				try:
					tmp, created = radreply.objects.get_or_create(username = i.mac)
				except (exceptions.ObjectDoesNotExist):
					return
	
	def __unicode__(self):
		return self.username

class device(models.Model):
	nom = models.CharField(max_length = 64)
	mac = models.CharField(max_length = 17)
	publisher = models.ForeignKey('Client')

	def save(self, *args, **kwargs):
		super(device, self).save(*args, **kwargs)
		b = Client.objects.get(pk = self.publisher.pk)
		if b.has_rezal:
			tmp, created = radcheck.objects.get_or_create(username = self.mac, attribute = "Auth-Type", op = ":=", value = "Accept")
		else:
			try:
				tmp = radcheck.objects.filter(username = self.mac)
				tmp.all().delete()
			except (exceptions.ObjectDoesNotExist, exceptions.MultipleObjectsReturned):
				return
		if b.is_conscrit:
			tmp, created = radreply.objects.get_or_create(username = self.mac)
