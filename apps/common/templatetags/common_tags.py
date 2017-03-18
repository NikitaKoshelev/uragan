# coding: utf-8
from django.template import Library

register = Library()

@register.filter
def verbose_name(object):
    return object._meta.verbose_name

