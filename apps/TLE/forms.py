# coding: utf-8

from django.forms import Form, DateTimeField, IntegerField


# class TleForms(ModelForm):
#    class Meta:
#        model = TLE

class TleApiForm(Form):
    datetime_start = DateTimeField()
    datetime_end = DateTimeField()
    satellite_id = IntegerField(min_value=0)
