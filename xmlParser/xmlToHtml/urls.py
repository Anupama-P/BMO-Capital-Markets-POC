from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.xml_to_html_parser, name='xml_to_html_parser'),
]
