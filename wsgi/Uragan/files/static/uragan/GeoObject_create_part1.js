/**
 * Created by koshelev on 14.05.15.
 */
var geocoder, map, marker,
    $title = $('id_title'),
    $lat = $("#id_lat"),
    $lon = $("#id_lon");

function initialize() {
    //Определение карты
    var latlng = new google.maps.LatLng(55.920963, 37.80495829999995);
    var options = {
        zoom: 12,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.HYBRID
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), options);

    //Определение геокодера
    geocoder = new google.maps.Geocoder();

    marker = new google.maps.Marker({map: map, draggable: true});

    //Добавляем слушателя события обратного геокодирования для маркера при его перемещении
    google.maps.event.addListener(marker, 'drag', function () {
        geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var cont = $('#select2-google_geocode-container');
                    cont.attr('title', results[0].formatted_address);
                    cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                    $lat.val(marker.getPosition().lat());
                    $lon.val(marker.getPosition().lng());
                }
            }
        });
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
                    $title.val(data.display_name);

                }
            }
        });


    })
}


$('#div_id_lon').after($('<div id="map_canvas" style="width:100%; height:600px; margin: 0 0"></div>'));

$lat.keyup(function (key) {
    var location = new google.maps.LatLng($(this).val(), $lon.val());
    marker.setPosition(location);
    geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var cont = $('#select2-nominatim_geocode-container, #select2-google_geocode-container');
                cont.attr('title', results[0].formatted_address);
                cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                $title.val(results[0].formatted_address);
            }
        }
    });
    map.setCenter(location);
});

$lon.keyup(function (key) {
    var location = new google.maps.LatLng($lat.val(), $(this).val());
    marker.setPosition(location);
    geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[0]) {
                var cont = $('#select2-nominatim_geocode-container, #select2-google_geocode-container');
                cont.attr('title', results[0].formatted_address);
                cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                $title.val(results[0].formatted_address);
            }
        }
    });
    map.setCenter(location);
});

initialize();
$('#create-geo_object').before($('<div class="row" id="geocoders"></div>'));


