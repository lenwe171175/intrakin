from django.contrib import admin
from kfet.models import inputmethod, entity, product, transactionpg

# Register your models here.

admin.site.register(inputmethod)
admin.site.register(product)
admin.site.register(entity)
admin.site.register(transactionpg)
