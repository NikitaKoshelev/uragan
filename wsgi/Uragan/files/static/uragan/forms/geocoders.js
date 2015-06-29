/**
 * Created by koshelev on 14.06.15.
 */

var $geocode_select2 = $('<select class="form-control" id="geocode_select2"></select>');

$(document).ready(function () {
    $geocode_select2.select2({
        placeholder: gettext('Search geo object with geocoders...'),
        allowClear: true,
        minimumInputLength: 2,
        language: page_language_code,
        width: '100%',

        query: function (query) {
            // here we check whether the user has entered some search term
            // and enforce a min term length to 2 chars
            var reverse_find = {text: gettext('Reverse find'), children: $geocode_select2.children().map(function (i, item){
                var elem = $(item);
                if (elem.text().search(query.term) !== -1) return optionToData(elem);
            })};
            if (query.term && query.term.length > 1)
                $.when(ajax_google_geocode(query.term),
                       ajax_nominatim_geocode(query.term),
                       ajax_geonames_geocode(query.term))
                    .done(function (g, n, gn) {
                              var select2data = {results: []};
                              if (reverse_find.children.length != 0) select2data.results.push(reverse_find);
                              //console.log(reverse_find.children.length, reverse_find);
                              select2data.results.push(ajax_nominatim_geocode.select2_format(n));
                              select2data.results.push(ajax_google_geocode.select2_format(g));
                              select2data.results.push(ajax_geonames_geocode.select2_format(gn));

                              query.callback(select2data);
                          });
            else if (reverse_find.children.length != 0) query.callback({results: [reverse_find]});
        },
        templateResult: function (geocode_select2) {
            if (geocode_select2.children && geocode_select2.children.length === 0) {
                //console.log(geocode_select2);
                return $('<span>{0} <small class="text-muted">{1}</small></span>'
                             .f(geocode_select2.text, gettext('Not found')));
            }
            else if (geocode_select2.loading || geocode_select2.children) return geocode_select2.text;
            else {
                return $('<strong>{0}</strong><span class="pull-right">({1}, {2})</span>'
                             .f(geocode_select2.text, geocode_select2.lat, geocode_select2.lon));
            }
        } // omitted for brevity, see the source of this page

        //templateSelection: function (geocode_select2) {
        //    return geocode_select2.text ? geocode_select2.text : gettext('Not found');
        //} // omitted for brevity, see the source of this page
    });
});

$('#geocoders')
    .append($('<div>', {class: 'form-group'})
                .append($('<label>', {for: "geocode", class: "control-label"})
                            .append('Geocoder'),
                        $geocode_select2)
);


$geocode_select2.on('select2:select', function (e) {
    //console.log(e);
    var geocode_select2 = e.params.data;
    var cont = $('#select2-geocode_select2-container'), title = geocode_select2.text;
    cont.attr('title', title);
    cont.html('<span class="select2-selection__clear">?</span>' + title);
    $("[id^=id_][id$=lat]").val(geocode_select2.lat);
    $("[id^=id_][id$=lon]").val(geocode_select2.lon);
    $("[id^=id_][id$=title]").val(geocode_select2.text);
    layer = new google.maps.KmlLayer({
        url: window.location.href.replace('create', 'kml') + '?title=' + encodeURI(title),
        map: map
    });
    console.log(layer);
    var location = new google.maps.LatLng(geocode_select2.lat, geocode_select2.lon);
    marker.setPosition(location);
    map.setCenter(location);

});


function ajax_google_geocode(term) {
    return $.getJSON("https://maps.googleapis.com/maps/api/geocode/json", {
        address: term,
        key: 'AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw',
        language: page_language_code
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
    return $.getJSON("http://nominatim.openstreetmap.org/search", {q: term, format: 'json', 'accept-language': page_language_code});
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
        lang: page_language_code
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

function optionToData(element) {
    //console.log(element);
        return {
            id: element.prop("value"),
            lat: element.prop("value").split(', ')[0].replace('(', ''),
            lon: element.prop("value").split(', ')[1].replace(')', ''),
            text: element.text(),
            element: element.get(),
            css: element.attr("class"),
            disabled: element.prop("disabled")
            //locked: equal(element.attr("locked"), "locked") || equal(element.data("locked"), true)
        };
}
