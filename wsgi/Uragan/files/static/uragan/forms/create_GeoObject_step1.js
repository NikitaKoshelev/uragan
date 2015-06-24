/**
 * Created by koshelev on 14.05.15.
 */


var geocoder, map, marker,
    $form = $('#create-geo_object'),
    $title = $form.find('[id^=id_][id$=title]'),
    $lat = $form.find("[id^=id_][id$=lat]"),
    $lon = $form.find("[id^=id_][id$=lon]"),
    $coords = $('<div class="row" id="coords"></div>'),
    $lon_container = $form.find('[id^=div_id_][id$=lon]'),
    $lat_container = $form.find('[id^=div_id_][id$=lat]');

$form.before($('<div class="form-row" id="geocoders"></div>'));

$coords.append($lat_container.addClass('col-sm-6'), $lon_container.addClass('col-sm-6'));
$form.find('[id^=div_id_][id$=title]').after($coords);

$('<div id="map_canvas" style="width:100%; height: {0}" ></div>'.f('800px'/*$('.content').css('height'))*/)).appendTo($form);

$lat.keyup(function (key) {
    var location = new google.maps.LatLng($(this).val(), $lon.val());
    marker.setPosition(location);
    google_reverse_geocode(location);
});

$lon.keyup(function (key) {
    var location = new google.maps.LatLng($lat.val(), $(this).val());
    marker.setPosition(location);
    google_reverse_geocode(location);
});

var $btn_reverse = $('<button class="btn btn-default pull-left" type="button"><i class="fa fa-search"></i> {0}</button>'
                         .f(gettext('Nominatim reverse geocode')));

$btn_reverse.appendTo($('#buttons')).click(function () {
    var location = new google.maps.LatLng($lat.val(), $lon.val());
    nominatim_reverse_geocode(location);
});

$(document).ready(async_gmaps());

/*************************************************Functions************************************************************/

function google_reverse_geocode(location) {

    map.setCenter(location);

    geocoder.geocode({'latLng': location}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                $('#nominatim_geocode').val('({0}, {1})'.f(results[0].geometry.lat(), results[0].geometry.lng())).trigger('change');

                var cont = $('#select2-google_geocode-container'),
                    title = results[0].formatted_address;
                //cont.attr('title', title);
                //cont.html('<span class="select2-selection__clear">×</span>' + title);
                $title.val(title);
                $lat.val(location.lat());
                $lon.val(location.lng());
                //showMessage(false, gettext('Was found geo object') + ': "{0}"'.f(title.bold().italics()));
            }
        }
    });
}

function nominatim_reverse_geocode(location) {

    $.ajax({
       url: "http://nominatim.openstreetmap.org/reverse",
       dataType: 'json',
       data: {lat: location.lat(), lon: location.lng(), format: 'json'},
       cache: true,
       ifModified: true,
       timeout: 300,
       success: function (data, status) {
           if (status === 'success') {
               var cont = $('#select2-nominatim_geocode-container'),title = data.display_name;
               cont.attr('title', title);
               cont.html('<span class="select2-selection__clear">×</span>' + title);
               $title.val(title);
           }
       }
    });
}


function initialize() {
    var location = $lat.val() && $lon.val() ?
        new google.maps.LatLng($lat.val(), $lon.val()) : new google.maps.LatLng(55.920963, 37.80495829999995);

    // Определение карты
    var options = {
        center: location,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), options);

    // Определение геокодера
    geocoder = new google.maps.Geocoder();

    // Отображаем положение маркера на форме
    marker = new google.maps.Marker({map: map, draggable: true});
    marker.setPosition(location);

    // Добавляем слушателя события обратного геокодирования для маркера при его перемещении
    google.maps.event.addListener(marker, 'drag', function () {
        google_reverse_geocode(marker.getPosition());
    });

}

/*****************************************************End functions****************************************************/






