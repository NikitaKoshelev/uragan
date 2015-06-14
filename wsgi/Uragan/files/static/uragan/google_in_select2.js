/**
 * Created by koshelev on 14.06.15.
 */

var $google_geocode = $('<select class="form-control" id="google_geocode"></select>');
$(document).ready(function () {
    $google_geocode.select2({
        placeholder: 'Search geo object with Google Geocoder...',
        allowClear: true,
        minimumInputLength: 3,

        ajax: {
            url: "https://maps.googleapis.com/maps/api/geocode/json",
            dataType: 'json',
            type: "GET",
            cache: true,
            data: function (params, page) {
                return {
                    address: params.term, // search term
                    key: 'AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw'
                };
            },
            processResults: function (data, params) {
                // parse the results into the format expected by Select2.
                // since we are using custom formatting functions we do not need to
                // alter the remote JSON data

                params.page = params.page || 1;

                // If your ajax response doesn't have id and text attributes you should fix them client side

                var select2data = data.results.map(function (obj) {
                    return {
                        id: '(' + obj.geometry.location.lat + ', ' + obj.geometry.location.lng + ')',
                        text: obj.formatted_address,
                        lat: obj.geometry.location.lat,
                        lon: obj.geometry.location.lng,
                        polygon: ''
                    };
                });

                return {
                    results: select2data
                };
            }
        },

        templateResult: function (google_geocode) {
            if (google_geocode.loading) {
                return google_geocode.text;
            }
            else {
                return $('<p><strong>' + google_geocode.text +'</strong><span class="pull-right">('
                    + google_geocode.lat + ', ' + google_geocode.lon + ')</span></p>');
            }

        } // omitted for brevity, see the source of this page

        //templateSelection: function (google_geocode) {
        //    return google_geocode.display_name;
        //} // omitted for brevity, see the source of this page
    });
});

$('#geocoders').append(
    //$('<div class="col-md-5"></div>').append(
    $('<div class="form-group col-md-5">' +
        '<label for="google_geocode" class="control-label">Google geocoder</label>' +
        '</div>').append(
        $google_geocode
    )
);


$google_geocode.on('select2:select', function (e) {
    var google_geocode = e.params.data;
    $("#id_lat").val(google_geocode.lat);
    $("#id_lon").val(google_geocode.lon);
    $("#id_title").val(google_geocode.text);
    $('#id_polygon').val(google_geocode.polygon);
    var location = new google.maps.LatLng(google_geocode.lat, google_geocode.lon);
    marker.setPosition(location);
    map.setCenter(location);

});
