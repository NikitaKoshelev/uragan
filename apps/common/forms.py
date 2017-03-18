# coding: utf-8
from django import forms

base_css = {
    'all': (
        'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css',
    )
}

base_js = (
    'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js',
    'uragan/forms/ajax_setup_csrf.js'
)


class BaseModelForm(forms.ModelForm):
    class Media:
        css = base_css
        js = base_js


class BaseForm(forms.Form):
    class Media:
        css = base_css
        js = base_js
