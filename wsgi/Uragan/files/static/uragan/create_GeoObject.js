/**
 * Created by koshelev on 14.05.15.
 */
var geocoder, map, marker,
    $title = $('#id_title'),
    $lat = $("#id_lat"),
    $lon = $("#id_lon"),
    $coords = $('<div class="row" id="coords"></div>'),
    $lon_container = $('#div_id_lon'),
    $lat_container = $('#div_id_lat');

$('#create-geo_object').before($('<div class="row" id="geocoders"></div>'));

$coords.append( $lat_container.addClass('col-sm-6'), $lon_container.addClass('col-sm-6'));
$('#div_id_title').after($coords);

$coords.after($('<div id="map_canvas" style="width:100%; height:600px; margin-bottom: 15px"></div>'));
initialize();


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

/*************************************************Functions************************************************************/

String.prototype.format = String.prototype.f = function () {
    var args = arguments;
    return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
        if (m == "{{") { return "{"; }
        if (m == "}}") { return "}"; }
        return args[n];
    });
};

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


function google_reverse_geocode(location){

    map.setCenter(location);

    geocoder.geocode({'latLng': location}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var cont = $('#select2-google_geocode-container'),
                    title = results[0].formatted_address;
                cont.attr('title', title);
                cont.html('<span class="select2-selection__clear">×</span>' + title);
                $title.val(title);
                showMessage(false, gettext('Was found geo object') +': "{0}"'.f(title.bold().italics()));
            }
        }
    });
}


function initialize() {
    // Определение карты
    var options = {
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), options);

    // Определение геокодера
    geocoder = new google.maps.Geocoder();

    marker = new google.maps.Marker({map: map, draggable: true});
    var location = new google.maps.LatLng(55.920963, 37.80495829999995);
    marker.setPosition(location);

    // Отображаем положение маркера на форме
    google_reverse_geocode(location);
    $lat.val(location.lat());
    $lon.val(location.lng());

    // Добавляем слушателя события обратного геокодирования для маркера при его перемещении
    google.maps.event.addListener(marker, 'drag', function() {
        var location = marker.getPosition();
        //$lat.val(location.lat());
        //$lon.val(location.lng());
        //google_reverse_geocode(location);

        geocoder.geocode({'latLng': location}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var cont = $('#select2-google_geocode-container');
                    cont.attr('title', results[0].formatted_address);
                    cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                    $lat.val(location.lat());
                    $lon.val(location.lng());
                    $title.val(results[0].formatted_address);
                }
            }
        });
        map.setCenter(location);
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





