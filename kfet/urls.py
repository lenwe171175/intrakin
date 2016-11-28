from django.conf.urls import patterns, include, url
from kfet.views import getPgs, addtrpg, summarytrpg

urlpatterns = [
	url(r'^getPgs/$', getPgs, name = "getPgs"),
	url(r'^addtrpg/$', addtrpg, name = "addtrpg"),
	url(r'^summarytrpg/$', summarytrpg, name = "summarytrpg"),
]
