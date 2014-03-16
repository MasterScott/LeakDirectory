from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")

def detail(request, receiver_id):
    return HttpResponse("%s" % receiver_id)
