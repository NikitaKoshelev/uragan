from django.conf import settings
from django.forms.widgets import mark_safe, TextInput, Textarea


class VerticalTextarea(Textarea):
    def render(self, name, value, attrs=None):
        style = attrs.get('style', '')
        attrs['style'] = style + 'resize: vertical;'
        return super(VerticalTextarea, self).render(name, value, attrs)


class ColorPickerWidget(TextInput):
    class Media:
        css = {
            'all': (
                'plugins/colorpicker/bootstrap-colorpicker.min.css',
            )
        }
        js = (
            'plugins/colorpicker/bootstrap-colorpicker.min.js',
            'uragan/forms/color_field_initialize.js',
        )

    def render(self, name, value, attrs=None):
        html = '<div class="input-group colorpicker-addon"><span class="input-group-addon"><i></i></span>%s</div>'
        return mark_safe(html % super(ColorPickerWidget, self).render(name, value, attrs))
