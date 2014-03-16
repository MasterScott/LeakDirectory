from django.shortcuts import render

from node.models import Node

def index(request):
    nodes = Node.objects.all()
    return render(request, 'index.html', 
                  {'nodes': nodes})

def detail(request, node_address):
    pass
