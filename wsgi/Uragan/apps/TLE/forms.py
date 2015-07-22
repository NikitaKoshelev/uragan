__author__ = 'koshelev'

from django.forms import ModelForm, Form, DateTimeField, IntegerField

from apps.TLE.models import TLE

#class TleForms(ModelForm):
#    class Meta:
#        model = TLE

class TleApiForm(Form):
    datetime_start = DateTimeField()
    datetime_end = DateTimeField()
    satellite_id = IntegerField(min_value=0)