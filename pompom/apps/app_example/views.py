# coding=utf-8
from django.http import HttpResponse


def hello_world(request, name):  # pylint: disable=unused-argument
    return HttpResponse("Hello, World: {name}".format(name=name))
