from django.shortcuts import render_to_response, redirect
from django.views.generic import CreateView, DeleteView, FormView
from formtools.wizard.views import CookieWizardView

from .models import GeoObject
from .forms import GeoObjectForm, GeoObjectFormStep1, GeoObjectFormStep2
from apps.common.mixins import LoginRequiredMixin


def where_iss(request):

    return render_to_response('includes/where_is_iss.html')


class CreateGeoObject(CreateView):
    form_class = GeoObjectForm

    template_name = 'GeoObject/GeoObject_form.html'



class WizardCreateGeoObject(CookieWizardView):
    template_name = 'GeoObject/wizard.html'
    form_list = (
        ('step1', GeoObjectFormStep1),
        ('step2', GeoObjectFormStep2),
    )

    def get_form_initial(self, step):
        init = {}
        if step == 'step2':
            init['polygon'] = super(WizardCreateGeoObject, self).get_cleaned_data_for_step('step1')['polygon']
        return self.initial_dict.get(step, init)

    def done(self, form_list, **kwargs):
        data = {k:v for form in form_list for k,v in form.cleaned_data.items()}
        GeoObject.objects.create(**data)
        return redirect('/admin/GeoObject/')
