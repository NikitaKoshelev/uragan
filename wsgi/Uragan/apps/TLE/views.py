from django.shortcuts import render
from django.views.generic import ListView

from requests import get
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
import time
from .models import TLE


class TLE_ListView(ListView):
    template_name = 'TLE/TLE_list.html'
    model = TLE
