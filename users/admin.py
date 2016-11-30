#-*- coding: utf-8 -*-
from django.contrib import admin
from users.models import Client, device, radcheck, radreply
from django.core import exceptions

# Register your models here.

class AdminClient(admin.ModelAdmin):
	list_display = ('nom','prenom','chambre','phone','mail','is_active','has_rezal','is_conscrit','is_gadz','is_superuser','credit')
	list_filter = ('is_active','has_rezal','is_conscrit','is_gadz','is_superuser','credit')
	search_fields = ('nom','prenom','chambre')
	actions = ['set_gadz', 'remove_gadz','set_rezal','remove_rezal','set_conscrit','remove_conscrit','set_actif','remove_actif','set_superuser','remove_superuser']

	def set_gadz(self, request, queryset):
		queryset.update(is_gadz = True)
	set_gadz.short_description = u"Activer les modules Gadz pour les utilisateurs sélectionnés"

	def set_rezal(self, request, queryset):
		queryset.update(has_rezal = True)
	set_rezal.short_description = u"Activer le Rézal pour les utilisateurs sélectionnés"

	def set_actif(self, request, queryset):
		queryset.update(is_active = True)
	set_actif.short_description = u"Activer les utilisateurs sélectionnés"

	def remove_actif(self, request, queryset):
		queryset.update(is_active = False)
		queryset.update(has_rezal = False)
		queryset.update(is_conscrit = False)
		for b in queryset:
			a = device.objects.filter(publisher = b.pk)
			for i in a:
				try:
					tmp = radcheck.objects.filter(username = i.mac)
					tmp.all().delete()
					tmp = radreply.objects.filter(username = i.mac)
					tmp.all().delete()
					i.delete()
				except (exceptions.ObjectDoesNotExist):
					return
	remove_actif.short_description = u"Désactiver les utilisateurs sélectionnés"

	def remove_gadz(self, request, queryset):
		queryset.update(is_gadz = False)
	remove_gadz.short_description = u"Désactiver les modules Gadz pour les utilisateurs sélectionnés"

	def remove_rezal(self, request, queryset):
		queryset.update(has_rezal = False)
		queryset.update(is_conscrit = False)
		for b in queryset:
			a = device.objects.filter(publisher = b.pk)
			for i in a:
				try:
					tmp = radcheck.objects.filter(username = i.mac)
					tmp.all().delete()
					tmp = radreply.objects.filter(username = i.mac)
					tmp.all().delete()
					i.delete()
				except (exceptions.ObjectDoesNotExist):
					return
	remove_rezal.short_description = u"Désactiver le Rézal pour les utilisateurs sélectionnés"
	
	def set_superuser(self, request, queryset):
		queryset.update(is_superuser = True)
		queryset.update(is_staff = True)
	set_superuser.short_description = u"Donner les droits d'admin à l'utilisateur sélectionné"

	def remove_superuser(self, request, queryset):
		queryset.update(is_superuser = False)
		queryset.update(is_staff = False)
	remove_superuser.short_description = u"Retirer les droits d'admin à l'utilisateur sélectionné"

	def set_conscrit(self, request, queryset):
		queryset.update(is_conscrit = True)
		for b in queryset:
			a = device.objects.filter(publisher = b.pk)
			for i in a :
				try:
					tmp, created = radreply.objects.get_or_create(username = i.mac)
				except (exceptions.ObjectDoesNotExist):
					return
	set_conscrit.short_description = u"Limiter la bande passante des utilisateurs sélectionnés"

	def remove_conscrit(self, request, queryset):
		queryset.update(is_conscrit = False)
		for b in queryset:
			a = device.objects.filter(publisher = b.pk)
			for i in a:
				try:
					tmp = radreply.objects.filter(username = i.mac)
					tmp.all().delete()
				except (exceptions.ObjectDoesNotExist):
					return
	remove_conscrit.short_description = u"Enlever la limitation de bandwidth des utilisateurs sélectionnés"

class Admindevice(admin.ModelAdmin):
	list_display = ('nom','mac','publisher')

admin.site.register(Client,AdminClient)
admin.site.register(device,Admindevice)
