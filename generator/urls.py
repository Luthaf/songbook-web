# -*- coding: utf-8 -*-

# A supprimer en prod.
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, url #,include
from generator.views import AfficherChant, ListeChantsParAuteur, ListeAuteurs

urlpatterns = patterns('generator.views',
    url(r'^$', 'home', name="home"),                   
    url(r'^songs/(?P<chanteur>.+)/$', ListeChantsParAuteur.as_view(), name="song_list_by_artist"),
    url(r'^songs/(?P<chanteur>.+)/(?P<slug>.+)/$', AfficherChant.as_view(), name='show_song'),
    url(r'^songs/$', ListeAuteurs.as_view(), name="artist_list"),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'generator/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}),    
)

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)