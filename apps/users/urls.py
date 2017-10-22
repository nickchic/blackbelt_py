from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^logout$', views.logout),
    url(r'^login_action$', views.login_action),
    url(r'^register_action$', views.register_action),
    url(r'^users/home$', views.user_home),
    url(r'^users/(?P<user_id>[0-9]+)', views.user_page),
    url(r'^add/(?P<user_id>[0-9]+)', views.add_friend),
    url(r'^remove/(?P<user_id>[0-9]+)', views.remove_friend),
    url(r'^friends', views.friends)
]
