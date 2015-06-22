/**
 * Created by koshelev on 14.06.15.
 */

var lng = navigator.browserLanguage || navigator.language || navigator.userLanguage,
    $google_geocode = $('<select class="form-control" id="geocode"></select>');

$(document).ready(function () {
    $google_geocode.select2({
        placeholder: gettext('Search geo object with geocoders...'),
        allowClear: true,
        minimumInputLength: 2,
        language: lng,
        width: '100%',

        query: function (query) {
            // here we check whether the user has entered some search term
            // and enforce a min term length to 2 chars
            if (query.term)
                $.when(ajax_google_geocode(query.term),
                       ajax_nominatim_geocode(query.term),
                       ajax_geonames_geocode(query.term))
                    .done(function (g, n, gn) {
                              var select2data = {
                                  results: [
                                      ajax_nominatim_geocode.select2_format(n),
                                      ajax_google_geocode.select2_format(g),
                                      ajax_geonames_geocode.select2_format(gn)
                                  ]
                              };
                              query.callback(select2data);
                          });
        },
        templateResult: function (google_geocode) {
            if (google_geocode.children && google_geocode.children.length === 0) {
                console.log(google_geocode);
                return $('<span>{0} <small class="text-muted">{1}</small></span>'
                             .f(google_geocode.text, gettext('Not found')));
            }
            else if (google_geocode.loading || google_geocode.children) return google_geocode.text;
            else {
                return $('<strong>{0}</strong><span class="pull-right">({1}, {2})</span>'
                             .f(google_geocode.text, google_geocode.lat, google_geocode.lon));
            }
        } // omitted for brevity, see the source of this page

        //templateSelection: function (google_geocode) {
        //    return google_geocode.text ? google_geocode.text : gettext('Not found');
        //} // omitted for brevity, see the source of this page
    });
});

$('#geocoders')
    .append($('<div>', {class: 'form-group'})
                .append($('<label>', {for: "google_geocode", class: "control-label"})
                            .append('Geocoder'),
                        $google_geocode)
);


$google_geocode.on('select2:select', function (e) {
    console.log(e);
    var google_geocode = e.params.data;
    var cont = $('#select2-google_geocode-container'), title = google_geocode.text;
    cont.attr('title', title);
    cont.html('<span class="select2-selection__clear">?</span>' + title);
    $("[id^=id_][id$=lat]").val(google_geocode.lat);
    $("[id^=id_][id$=lon]").val(google_geocode.lon);
    $("[id^=id_][id$=title]").val(google_geocode.text);
    $("[id^=id_][id$=polygon]").val(google_geocode.polygon);
    var layer = new google.maps.KmlLayer({
        url: '{0}//{1}/geo-object/kml/?title={2}'.f(window.location.protocol, window.location.host, encodeURI(title))
    });
    layer.setMap(map);
    var location = new google.maps.LatLng(google_geocode.lat, google_geocode.lon);
    marker.setPosition(location);
    map.setCenter(location);

});


function ajax_google_geocode(term) {
    return $.getJSON("https://maps.googleapis.com/maps/api/geocode/json", {
        address: term,
        key: 'AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw',
        language: lng
    });
}

ajax_google_geocode.select2_format = function (data) {
    return {
        text: 'Google', children: data[0].results.map(function (obj) {
            return {
                id: '({0}, {1})'.f(obj.geometry.location.lat, obj.geometry.location.lng),
                text: obj.formatted_address,
                lat: obj.geometry.location.lat,
                lon: obj.geometry.location.lng,
                polygon: ''
            };
        })
    }
};

function ajax_nominatim_geocode(term) {
    return $.getJSON("http://nominatim.openstreetmap.org/search", {q: term, format: 'json', 'accept-language': lng});
}

ajax_nominatim_geocode.select2_format = function (data) {
    return {
        text: 'Nominatim', children: data[0].map(function (obj) {
            return {
                id: '({0}, {1})'.f(obj.lat, obj.lon),
                text: obj.display_name,
                lat: obj.lat,
                lon: obj.lon
            };
        })
    }
};

function ajax_geonames_geocode(term) {
    return $.getJSON('http://ws.geonames.org/searchJSON', {
        q: term,
        username: 'nikita.koshelev',
        maxRows: 10,
        lang: lng
    })
}

ajax_geonames_geocode.select2_format = function (data) {
    return {
        text: 'GeoNames', children: data[0].geonames.map(function (obj) {
            if (obj) {
                return {
                    id: '({0}, {1})'.f(obj.lat, obj.lng),
                    text: obj.name,
                    lat: obj.lat,
                    lon: obj.lng,
                    polygon: ''
                };
            }
        })
    }
};