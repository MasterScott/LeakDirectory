import json

from leakdirectory.tasks import update_node

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def ping(request):
    try:
        r = json.loads(request.body)
        update_node(r['hidden_service'])
        response = {'status': 'updated'}
    except Exception as exc:
        print exc
        response = {'status': 'invalid-request'}
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
