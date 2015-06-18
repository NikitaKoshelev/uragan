/**
 * Created by koshelev on 15.06.15.
 */

var html = '<div class="box box-solid collapsed-box" id="translate_container">';
html += '<div class="box-header with-border">';
html += '<h3 class="box-title">' + gettext("Translator") + '</h3>';
html += '<div class="box-tools pull-right">';
html += '<button id="sync_toggle" class="btn btn-box-tool" data-toggle="tooltip" data-status="true" title="' + gettext('Sync translate') + '">';
html += '<i class="fa fa-toggle-on text-olive"></i>';
html += '</button>';
html += '<button id="reverse_btn" class="btn btn-box-tool" data-toggle="tooltip" title="' + gettext('Reverse') + '">';
html += '<i class="fa fa-exchange"></i>';
html += '</button>';
html += '<button class="btn btn-box-tool" data-widget="collapse" data-toggle="tooltip" title="' + gettext('Collapse') + '">';
html += '<i class="fa fa-minus"></i>';
html += '</button>';
html += '<button class="btn btn-box-tool" data-widget="remove" data-toggle="tooltip" title="' + gettext('Remove') + '">';
html += '<i class="fa fa-times"></i>';
html += '</button>';
html += '</div>';
html += '</div>';
html += '<div class="box-body">';
html += '<div class="row">';
html += '<div class="col-sm-6">';
html += '<div class="form-group">';
html += '<label for="source_select" class="control-label">' + gettext('Source language') + '</label>';
html += '<select id="source_select" class="form-control" style="width: 100%"></select>';
html += '</div>';
html += '<div class="form-group">';
html += '<label for="source" class="control-label sr-only">' + gettext('Source language') + '</label>';
html += '<textarea id="source" class="form-control" rows="1" style="resize: vertical"></textarea>';
html += '</div>';
html += '</div>';
html += '<div class="col-sm-6">';
html += '<div class="form-group">';
html += '<label for="translate_select" class="control-label">' + gettext('Destination language') + '</label>';
html += '<select id="translate_select" class="form-control" style="width: 100%"></select>';
html += '</div>';
html += '<div class="form-group">';
html += '<label for="destination" class="control-label sr-only">' + gettext('Destination language') + '</label>';
html += '<textarea id="destination" class="form-control" rows="1" style="resize: vertical"></textarea>';
html += '</div>';
html += '</div>';
html += '</div>';
html += '<div class="row">';
html += '<div class="col-xs-12" style="display: none;">';
html += '<button id="translate_btn" class="btn btn-flat btn-block btn-default">' + gettext("Translate") + '</button>';
html += '</div>';
html += '</div>';
html += '</div>';
html += '</div>';

$('#yandex_translate').append($(html));


var $translate_container = $('#translate_container'),
    $source_select = $($translate_container.find('#source_select')),
    $source = $($translate_container.find('textarea')[0]),
    $destination = $($translate_container.find('textarea')[1]),
    $translate_select = $($translate_container.find('#translate_select')),
    $sync_toggle = $($translate_container.find('#sync_toggle')),
    $translate_btn = $($translate_container.find('#translate_btn')),
    $reverse_btn = $($translate_container.find('#reverse_btn')),
    lng = navigator.browserLanguage || navigator.language || navigator.userLanguage;

lng = lng.split('-')[0];

$(document).ready(function () {
    $.getJSON('https://translate.yandex.net/api/v1.5/tr.json/getLangs', {
        key: 'trnsl.1.1.20150415T224006Z.a368509643fb7c76.cf232c7e8dce21c5295d69dfcd16ee2e76aa1cf9',
        ui: lng
    }, function (data) {
        var langs = [];
        $.each(data.langs, function (key, value) {
            langs.push({id: key, text: value})
        });
        $translate_select.select2({data: langs, language: lng});
        $translate_select.val(lng === 'en' ? 'ru': 'en').change();

        langs.push({id: 'auto', text: 'Determine automatically'});
        $source_select.select2({data: langs, language: lng});
        $source_select.val('auto').change();
    });
});


$('#translate_icon').click(function () {
    $translate_container.slideToggle('fast');
});


$source.keyup(function (eventObject) {
    if ($sync_toggle.data().status) yandex_translate($source.val());
});

$sync_toggle.click(function () {
    if ($sync_toggle.data().status) {
        $sync_toggle.data('status', false);
        $sync_toggle.find('i').removeClass('fa-toggle-on text-olive').addClass('fa-toggle-off text-red');
    }
    else {
        $sync_toggle.data('status', true);
        $sync_toggle.find('i').removeClass('fa-toggle-off text-red').addClass('fa-toggle-on text-olive');
    }
    $translate_btn.parent().slideToggle('fast');

});

$translate_btn.click(function () {
    yandex_translate($source.val());
});

$reverse_btn.click(function () {
    var s = $source_select.val(),
        d = $translate_select.val();
    $source_select.val(d).change();
    $translate_select.val(s === 'auto' ? lng : s).change();
});

function yandex_translate(text) {
    var s_lng = $source_select.val(),
        d_lng = $translate_select.val(),
        lng = s_lng === 'auto' ? d_lng : s_lng + '-' + d_lng;

    $.getJSON('https://translate.yandex.net/api/v1.5/tr.json/translate', {
        key: 'trnsl.1.1.20150415T224006Z.a368509643fb7c76.cf232c7e8dce21c5295d69dfcd16ee2e76aa1cf9',
        text: text,
        lang: lng,
        options: s_lng === 'auto' ? 1 : 0
    }, function (data, status) {
        $destination.val(data.text[0]);
    });
}
