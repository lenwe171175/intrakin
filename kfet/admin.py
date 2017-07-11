from django.contrib import admin
from kfet.models import inputmethod, entity, product, transactionpg, transactionvp, transactionboulc

# Register your models here.

class Admintransactionpg(admin.ModelAdmin):
	list_display = ('source','target','amount','accepted')

#admin.site.register(inputmethod)
#admin.site.register(product)
#admin.site.register(entity)
#admin.site.register(transactionpg, Admintransactionpg)
#admin.site.register(transactionvp)
#admin.site.register(transactionboulc)