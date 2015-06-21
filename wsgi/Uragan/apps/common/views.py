# coding: utf-8

from goslate import Goslate
from django.http import HttpResponse
import json


def GetModelData(form, fields):
    """
    Extract data from the bound form model instance and return a
    dictionary that is easily usable in templates with the actual
    field verbose name as the label, e.g.

    model_data{"Address line 1": "32 Memory lane",
               "Address line 2": "Brainville",
               "Phone": "0212378492"}

    This way, the template has an ordered list that can be easily
    presented in tabular form.
    """
    model_data = {}
    for field in fields:
        model_data[form[field].label] = "form.data.%s" % form[field].name
    return model_data


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