from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.default),
    url(r'^login$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^register$', views.register),
    url(r'^login$', views.index),
    url(r'^logout$', views.logout),
    url(r'^jobs/new$', views.createjob),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^unjoin/(?P<id>\d+)$', views.unjoin),
    url(r'^jobs/edit/(?P<id>\d+)$', views.editjob),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^jobs/(?P<id>\d+)$', views.renderme)
]