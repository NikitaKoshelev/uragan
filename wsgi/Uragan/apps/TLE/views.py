from django.shortcuts import render
from django.views.generic import ListView
from apps.TLE.models import TLE

class TLE_ListView(ListView):
    template_name = 'TLE/TLE_list.html'
    model = TLE


