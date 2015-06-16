__author__ = 'koshelev'
from django import forms

base_css = {
    'all': (
        'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.min.css',
        'plugins/select2/css/select2.min.css',
    )
}

base_js = (
    'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js',
    'plugins/select2/js/select2.full.min.js',
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
