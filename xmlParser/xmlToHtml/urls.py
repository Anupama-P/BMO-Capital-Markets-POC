from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search_view, name='search'),
    url(r'^search/$', views.search),
    url(r'^search_filter/$', views.search_filter),
    url(r'^(?P<doc_name>[0-9a-zA-Z]+)/$', views.show_document),
    # url(r'^company/(?P<company>[0-9a-zA-Z]+)/$', views.show_company),
]
