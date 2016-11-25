from django.conf.urls import patterns, include, url
from kfet.views import getPgs, transactionpg

urlpatterns = [
	url(r'^getPgs/$', getPgs, name = "getPgs"),
	url(r'^transactionpg/$', transactionpg, name = "transactionpg"),
]
