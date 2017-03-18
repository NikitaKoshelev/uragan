from django.forms import TextInput, Textarea, Select, SelectMultiple, DateTimeInput
from django.forms.widgets import mark_safe, Input


class ColorPickerWidget(TextInput):
    class Media:
        css = {
            'all': (
                'plugins/colorpicker/bootstrap-colorpicker.min.css',
            )
        }
        js = (
            'plugins/colorpicker/bootstrap-colorpicker.min.js',
        )

    def render(self, name, value, attrs=None):
        html = '<div class="input-group colorpicker-addon"><span class="input-group-addon"><i></i></span>%s</div>'
        html += ('<script type="application/javascript" defer>'
                 '$(document).ready('
                 'function () { $(".colorpicker-addon").colorpicker({align: "left", format: "hex"}); '
                 '});</script>')
        return mark_safe(html % super(ColorPickerWidget, self).render(name, value, attrs))


class StaticWidget(Input):
    def render(self, name, value, attrs=None):
        html = '<p class="form-control-static">%s</p>' % value
        return mark_safe(html)


class WYSIHTML5Widget(Textarea):
    class Media:
        css = {
            'all': (
                'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.css',
            )
        }
        js = (
            'plugins/bootstrap-wysihtml5/bootstrap3-wysihtml5.all.min.js',
        )

    def render(self, name, value, attrs=None):
        html = super(WYSIHTML5Widget, self).render(name, value, attrs)
        html += ('<script type="application/javascript" defer>'
                 '$(document).ready(function () {{$("#id_{0}").wysihtml5()}});'
                 '</script>'.format(name))
        return mark_safe(html)


class AutosizedTextarea(Textarea):
    """
    Autosized Textarea - textarea height dynamically grows based on user input
    """

    class Media:
        js = ('plugins/jquery.autosize.min.js',)

    def render(self, name, value, attrs=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            '<script type="text/javascript">'
            '$(document).ready(function () { $("#id_%s").attr("rows", 1).autosize().css("resize", "vertical"); });'
            '</script>'
            % name)
        return output


class Select2Widget(Select):
    # class Media:
    #    css = {'all': ('plugins/select2/css/select2.min.css',)}
    #    js = ('plugins/select2/js/select2.full.min.js',)

    def render(self, name, value, attrs=None, choices=()):
        html = super(Select2Widget, self).render(name, value, attrs=None, choices=())
        html += ('<script type="text/javascript">'
                 '$(document).ready(function () { '
                 '$("[name=%s]").select2({language: page_language_code, width: "100%%"}); });'
                 '</script>' % name)
        return html


class MultipleSelect2Widget(SelectMultiple):
    # class Media:
    #    css = {'all': ('plugins/select2/css/select2.min.css',)}
    #    js = ('plugins/select2/js/select2.full.min.js',)

    def render(self, name, value, attrs=None, choices=()):
        html = super(MultipleSelect2Widget, self).render(name, value, attrs, choices=())
        html += ('<script type="text/javascript">'
                 '$(document).ready(function () { '
                 '$("#id_%s").select2({language: page_language_code, width: "100%%"});});'
                 '</script>' % name)
        return html


class DateTimePickerWidget(DateTimeInput):
    class Media:
        css = {'all': ('plugins/bootstrap-datetimepicker-4.14.30/css/bootstrap-datetimepicker.min.css',)}
        js = (
            'plugins/bootstrap-datetimepicker-4.14.30/js/moment-with-locales.min.js',
            'plugins/bootstrap-datetimepicker-4.14.30/js/bootstrap-datetimepicker.min.js',
        )

    def render(self, name, value, attrs=None):
        base = super(DateTimePickerWidget, self).render(name, value, attrs)
        html = ('<div class="input-group date" id="input_group_%s">'
                '%s <span class="input-group-addon"><span class="fa fa-clock-o"></span></span>'
                '</div>' % (name, base))
        html += ('<script type="text/javascript">'
                 '$(document).ready(function () { '
                 '$("#input_group_%s").datetimepicker({'
                 '  locale: page_language_code,'
                 '  icons: {'
                 '      time: "fa fa-clock-o",'
                 '      date: "fa fa-calendar",'
                 '      up: "fa fa-arrow-up",'
                 '      down: "fa fa-arrow-down"'
                 '  }'
                 '}); });'
                 '</script>' % name)
        return html
