from django.conf import settings
from django.forms.widgets import mark_safe, TextInput


class ColorPickerWidget(TextInput):
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'plugins/colorpicker/bootstrap-colorpicker.min.css',)
        }
        js = (settings.STATIC_URL + 'plugins/colorpicker/bootstrap-colorpicker.min.js',
              settings.STATIC_URL + 'plugins/colorpicker/color_widget.js',)

    def render(self, name, value, attrs=None):
        html = """
        <div class="input-group colorpicker-addon">
            {}
            <span class="input-group-addon"><i></i></span>
        </div>
        """.format(super(ColorPickerWidget, self).render(name, value, attrs))
        return mark_safe(html)