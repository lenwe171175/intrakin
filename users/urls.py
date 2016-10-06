from django.conf.urls import patterns, include, url
from users.views import index, loginPage, inscription, settings, add_mac, show_mac
from django.contrib.auth.views import logout, password_change, password_change_done
urlpatterns = [
	url(r'^$', index, name = 'index'),
	url(r'^login/$', loginPage, name = 'login'),
	url(r'^sign-out/$', logout, {'next_page': '/'}, name = 'sign-out'),
	url(r'^inscription/$', inscription, name = 'inscription'),
	url(r'^settings/$', settings, name = 'settings'),
	url(r'^addmac/$', add_mac, name = 'addmac'),
	url(r'^showmac/$', show_mac, name= 'showmac'),
	url(r'^password_change/$', password_change, name = "password_change"),
	url(r'^password_change_done/$', password_change_done, name = "password_change_done"),
]
