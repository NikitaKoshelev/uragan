# coding: utf-8
from django.views.generic.base import TemplateResponseMixin

from .models import Satellite


class SatellitesTemplateResponseMixin(TemplateResponseMixin):
    def get_satellites_list(self):
        return Satellite.objects.values('pk', 'title')

    def render_to_response(self, context, **response_kwargs):
        context.update({'satellites_list': self.get_satellites_list()})
        return super(SatellitesTemplateResponseMixin, self).render_to_response(context, **response_kwargs)
