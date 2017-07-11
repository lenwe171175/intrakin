from django.conf.urls import patterns, include, url
from users.views import index, loginPage, inscription, settings, add_mac, show_mac, macapprobation, macdeletion, contactform, admincontrols, about
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout

urlpatterns = [
	url(r'^$', index, name = 'index'),
	url(r'^login/$', loginPage, name = 'login'),
	url(r'^sign-out/$', logout, {'next_page': '/'}, name = 'sign-out'),
	url(r'^inscription/$', inscription, name = 'inscription'),
	url(r'^settings/$', settings, name = 'settings'),
	url(r'^addmac/$', add_mac, name = 'addmac'),
	url(r'^showmac/$', show_mac, name= 'showmac'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^macapprobation/$', macapprobation, name='macapprobation'),
    url(r'^macdeletion/$', macdeletion, name='macdeletion'),
    url(r'^contactform/$', contactform, name='contactform'),
    url(r'^admincontrols/$', admincontrols, name='admincontrols'),
    url(r'^about/$', about, name='about'),
]
