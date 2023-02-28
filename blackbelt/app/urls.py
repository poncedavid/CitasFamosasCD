
from . import views
from django.urls import include, re_path

                    
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^register$', views.register),
    re_path(r'^login$', views.login),
    re_path(r'^logout$', views.logout),
    re_path(r'^quotes$', views.quotes),
    re_path(r'^quotes/(?P<quote_id>\d+)/like$', views.likes),
    re_path(r'^quotes/(?P<quote_id>\d+)/unlike$', views.unlikes),

    re_path(r'^myaccount/(?P<user_id>\d+)$', views.edit),
    re_path(r'^user/(?P<user_id>\d+)$', views.show),
    re_path(r'^quotes/(?P<quote_id>\d+)/delete$', views.delete)
]