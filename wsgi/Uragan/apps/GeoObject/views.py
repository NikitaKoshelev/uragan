from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, FileResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DeleteView, FormView, DetailView
from django.utils.text import slugify
from formtools.wizard.views import CookieWizardView
import tempfile
from .models import GeoObject
from .forms import GeoObjectForm, GeoObjectFormStep1, GeoObjectFormStep2
from apps.common.mixins import LoginRequiredMixin
from goslate import Goslate


def where_iss(request):

    return render_to_response('includes/where_is_iss.html')


def get_kml(request, pk):

    try:
        obj = GeoObject.objects.get(pk=pk)
        polygon = obj.get_polygon_in_kml()#.decode()
        response = HttpResponse(polygon)
        filename = Goslate().translate(obj.title, target_language='en')
        response['Content-Disposition'] = 'attachment; filename="{}.kml"'.format(filename)
        print(obj.title, response['Content-Disposition'])
        return response
    except:
        return HttpResponse('GeoObject not found')



class DetailGeoObject(DetailView):
    model = GeoObject
    context_object_name = 'geo_object'
    template_name = 'GeoObject/GeoObject_detail.html'



class WizardCreateGeoObject(CookieWizardView):
    template_name = 'GeoObject/wizard.html'
    form_list = (GeoObjectFormStep1, GeoObjectFormStep2)

    def done(self, form_list, **kwargs):
        data = {k:v for form in form_list for k,v in form.cleaned_data.items()}

        pk = GeoObject.objects.create(**data).pk
        return redirect('GeoObject:detail', pk=pk)
