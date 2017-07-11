from django.conf.urls import patterns, include, url
from kfet.views import getPgs, addtrpg, summarytrpg, cashinputview, getProducts, seuilpg, histopg, bucquageboulc, productcreation, productdisplay, productedit

urlpatterns = [
	url(r'^getPgs/$', getPgs, name = "getPgs"),
	url(r'^addtrpg/$', addtrpg, name = "addtrpg"),
	url(r'^summarytrpg/$', summarytrpg, name = "summarytrpg"),
	url(r'^cashinput/$', cashinputview, name = "cashinput"),
	url(r'^seuilpg/$', seuilpg, name = "seuilpg"),
	url(r'^histopg/$', histopg, name = "histopg"),
	url(r'^getProducts/$', getProducts, name = "getProducts"),
	url(r'^bucquageboulc/$', bucquageboulc, name = "bucquageboulc"),
	url(r'^productcreation/$', productcreation, name = "productcreation"),
	url(r'^productdisplay/$', productdisplay, name= "productdisplay"),
	url(r'^productedit/(?P<id_product>\d+)$', productedit, name="productedit"),
]
