/**
 * Created by koshelev on 14.05.15.
 */


$('#div_id_title').append($('<select class="form-control" id="geo_object"></select>'));

var $geo_object;
$geo_object = $('#geo_object').select2({
    placeholder: 'Search geo object...',
    allowClear: true,
    minimumInputLength: 3,

    ajax: {
        url: "http://nominatim.openstreetmap.org/search",
        dataType: 'json',
        delay: 1000,
        type: "GET",
        cache: true,
        data: function (params, page) {
            return {
                q: params.term, // search term
                format: 'json',
                polygon_kml: 1
               // page: page || 1
            };
        },
        processResults: function (data, params) {
            // parse the results into the format expected by Select2.
            // since we are using custom formatting functions we do not need to
            // alter the remote JSON data

            params.page = params.page || 1;

            // If your ajax response doesn't have id and text attributes you should fix them client side
            var select2Data = $.map(data, function (obj) {
                obj.id = obj.place_id;

                obj.text = obj.display_name;
                return obj;
            });

            return {
                results: data
            };
        }
    },

    escapeMarkup: function (markup) {
        if (markup){
            var mark = $('<p>' + markup + '</p>');
            return mark;
        }

    }, // let our custom formatter work

    templateResult: function (geo_object) {
        if (geo_object.loading) return geo_object.text;
        console.log(geo_object);
        return $('<div class="row">' +
               '  <div class="col-md-9">' + geo_object.display_name + '</div>' +
               '  <div class="col-md-3">(' + geo_object.lat +', ' + geo_object.lon + ')</div>' +
               '</div>');
    }, // omitted for brevity, see the source of this page

    templateSelection: function (geo_object) {
        return geo_object.display_name;
    } // omitted for brevity, see the source of this page
});

$geo_object.on('select2:select', function (e) {
    var geo_object = e.params.data;
    console.log(geo_object);
    $("#id_lat").val(geo_object.lat);
    $("#id_lon").val(geo_object.lon);
    $("#id_title").val(geo_object.display_name);
    var location = new google.maps.LatLng(geo_object.lat, geo_object.lon);
    //var myParser = new geoXML3.parser({map: map});
    //myParser.parseKmlString(geo_object.geokml);
    marker.setPosition(location);
    map.setCenter(location);

});

$("#id_lat").keyup(function (key){
    var location = new google.maps.LatLng($(this).val(), $("#id_lon").val());
    marker.setPosition(location);
    geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var cont =  $('#select2-geo_object-container');
                    cont.attr('title',results[0].formatted_address);
                    cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                    $('id_title').val(results[0].formatted_address);
                }
            }
        });
    map.setCenter(location);
});

$("#id_lon").keyup(function (key){
    var location = new google.maps.LatLng($("#id_lat").val(), $(this).val());
    marker.setPosition(location);
    geocoder.geocode({'latLng': marker.getPosition()}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var cont =  $('#select2-geo_object-container');
                    cont.attr('title',results[0].formatted_address);
                    cont.html('<span class="select2-selection__clear">×</span>' + results[0].formatted_address);
                    $('id_title').val(results[0].formatted_address);
                }
            }
        });
    map.setCenter(location);
});



var geocoder, map, marker;

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
                    var cont =  $('#select2-geo_object-container');
                    cont.attr('title',results[0].formatted_address);
                    cont.html('<span class="select2-selection__clear">×</span>' +
                                                            results[0].formatted_address);
                    $('id_title').val(results[0].formatted_address);
                    $('#id_lat').val(marker.getPosition().lat());
                    $('#id_lon').val(marker.getPosition().lng());
                }
            }
        });
    });
}


