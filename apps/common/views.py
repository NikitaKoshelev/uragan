# coding: utf-8

from goslate import Goslate
from django.http import HttpResponse
import json

def translate_string(request):
    print(request.GET)
    if request.is_ajax():
        source = request.GET.get('source', False)
        if source:
            go = Goslate()
            result = {'result': go.translate(source, 'en')}
            print(source, result)
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            HttpResponse(json.dumps({'result': ''}), content_type='application/json')