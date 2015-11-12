from django.shortcuts import render
from django.http import HttpResponse
from .parser import parser


def index(request):
    return HttpResponse("Hello, world. You're at the mainpage")


def fetchScheludes(request):
    success = parser.fetchScheludes()
    return HttpResponse("Something happened. Success: " + str(success))
    