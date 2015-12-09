from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.searchSimpleScheludes, name='index'),
    url(r'^search$', views.searchSimpleScheludes, name='search'),
]