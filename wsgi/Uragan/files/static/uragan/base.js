var page_language_code = window.location.pathname.split('/', 2)[1] === 'en' ? 'en' : 'ru',
    page_language = page_language_code === 'en' ? 'English' : 'Russian';

$(document).ready(function () {
    var $manage_buttons = $('#manage_buttons'),
        active_items = $(".sidebar li:has(a[href$='{0}'])".f(window.location.pathname));

    active_items.addClass('active');

    if ($manage_buttons.html().trim()) $manage_buttons.show();

    //$('textarea.form-control').css('resize', 'vertical').attr('rows', 1);

    $('.required-field')
        .parent($('div'))
        .append($('<small>').addClass('pull-right text-yellow').html(gettext('*Required field').italics()));

    $('[data-toggle="popover"]').popover();
    $(".select2-container").removeClass("form-control");

});


function async_gmaps() {
    $('<script>', {
        type: 'text/javascript',
        src: 'http://maps.googleapis.com/maps/api/js?key=AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw&sensor=false&callback=initialize' +
        '&language=' + page_language_code
    }).appendTo($('body'));
}


function showMessage(hasError, messages) {

    var $messages_container = $('#messages'),
        $baseMessages = $messages_container.find('.alert'),
        divClass = hasError ? 'alert-danger' : 'alert-success',
        iClass = hasError ? 'fa-ban' : 'fa-check',
        bText = hasError ? gettext('Error!') : gettext('Success!'),
        $message = $('<div>', {'class': 'alert alert-dismissable ' + divClass});

    $message
        .append($('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>'))
        .append($('<h4>').append($('<i>', {'class': 'fa ' + iClass}), ' ' + bText))
        .append(messages)
        .fadeIn();

    $baseMessages.length !== 0 ? $baseMessages.first().before($message) : $message.appendTo('#messages');
    //$messages_container.show();
}


String.prototype.format = String.prototype.f = function () {
    var args = arguments;
    return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
        if (m == "{{") {
            return "{";
        }
        if (m == "}}") {
            return "}";
        }
        return args[n];
    });
};