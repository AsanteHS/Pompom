#! coding: utf-8

from django.conf.urls import url

from pompom.apps.app_example.views import hello_world

urlpatterns = [  # pylint: disable=invalid-name
    url(r'hello/(?P<name>[\w\-]+)/', hello_world),
]
