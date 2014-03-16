import re
import json

from leakdirectory.tasks import update_node

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

class InvalidAddress(Exception): pass

@csrf_exempt
def ping(request):
    try:
        r = json.loads(request.body)
        if not re.match('http:\/\/[a-z0-9]{16}.onion', r['hidden_service']):
            raise InvalidAddress
        update_node(r['hidden_service'])
        response = {'status': 'updated'}
    except InvalidAddress:
        response = {'status': 'invalid-address'}
    except Exception as exc:
        print exc
        response = {'status': 'invalid-request'}
    return HttpResponse(json.dumps(response),
                        content_type="application/json")
