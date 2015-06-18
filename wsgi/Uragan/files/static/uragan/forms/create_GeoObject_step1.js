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

$form.find('[id^=div_id_][id$=title]').before($('<div class="row" id="geocoders"></div>'));
$form.find('[id^=div_id_][id$=polygon]').hide();

$coords.append($lat_container.addClass('col-sm-6'), $lon_container.addClass('col-sm-6'));
$form.find('[id^=div_id_][id$=title]').after($coords);

$('<div id="map_canvas" style="width:100%; height: {0}" ></div>'.f($('.content').css('height'))).appendTo($form);

$lat.keyup(function (key) {
    var location = new google.maps.LatLng($(this).val(), $lon.val());
    marker.setPosition(location);
    google_reverse_geocode(location);
});

$lon.keyup(function (key) {
    var location = new google.maps.LatLng($lat.val(), $(this).val());
    marker.setPosition(location);
    google_reverse_geocode();
});

$(document).ready(initialize());

/*************************************************Functions************************************************************/

function google_reverse_geocode(location) {

    map.setCenter(location);

    geocoder.geocode({'latLng': location}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var cont = $('#select2-google_geocode-container'),
                    title = results[0].formatted_address;
                cont.attr('title', title);
                cont.html('<span class="select2-selection__clear">×</span>' + title);
                $title.val(title);
                $lat.val(location.lat());
                $lon.val(location.lng());
                showMessage(false, gettext('Was found geo object') + ': "{0}"'.f(title.bold().italics()));
            }
        }
    });
}


function initialize() {
    var location = new google.maps.LatLng(55.920963, 37.80495829999995);

    // Определение карты
    var options = {
        center: location,
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), options);

    // Определение геокодера
    geocoder = new google.maps.Geocoder();

    marker = new google.maps.Marker({map: map, draggable: true});
    //marker.setPosition(location);

    // Отображаем положение маркера на форме
    //google_reverse_geocode(location);
    //$lat.val(location.lat());
    //$lon.val(location.lng());

    // Добавляем слушателя события обратного геокодирования для маркера при его перемещении
    google.maps.event.addListener(marker, 'drag', function () {
        var location = marker.getPosition();

        google_reverse_geocode(location);

        //geocoder.geocode({'latLng': location}, function (results, status) {
        //    if (status == google.maps.GeocoderStatus.OK) {
        //        if (results[0]) {
        //            var cont = $('#select2-google_geocode-container');
        //            cont.attr('title', results[0].formatted_address);
        //            cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
        //            $lat.val(location.lat());
        //            $lon.val(location.lng());
        //            $title.val(results[0].formatted_address);
        //        }
        //    }
        //});
        //map.setCenter(location);
    });

}

/*****************************************************End functions****************************************************/


/**********************************************************************************************************************
 // Nominatim reverse geocoder

 $.ajax({
    url: "http://nominatim.openstreetmap.org/reverse",
    dataType: 'json',
    data: {lat: marker.getPosition().lat(), lon: marker.getPosition().lng(), format: 'json'},
    cache: true,
    ifModified: true,
    timeout: 300,
    success: function (data, status) {
        if (status === 'success') {
            var cont = $('#select2-nominatim_geocode-container');
            cont.attr('title', data.display_name);
            cont.html('<span class="select2-selection__clear">×</span>' + data.display_name);
        }
    }
});
 *********************************************************************************************/





