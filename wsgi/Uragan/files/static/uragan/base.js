var $manage_buttons = $('#manage_buttons');

if (!$manage_buttons.html().trim()) $manage_buttons.hide();

$('textarea').css('resize', 'vertical').attr('rows', 1);

$('.required-field')
    .parent($('div'))
    .append($('<small>').addClass('pull-right text-yellow').html(gettext('*Required field').italics()));

$.getJSON('/TLE/api/satellite_list', function (data, status){
    console.log(data);
});




