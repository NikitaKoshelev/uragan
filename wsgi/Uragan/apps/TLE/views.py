from django.shortcuts import render
from django.views.generic import ListView
from apps.TLE.models import TLE

class TLE_ListView(ListView):
    model = TLE
    paginate_by = 10
    template_name = 'TLE/list.html'


