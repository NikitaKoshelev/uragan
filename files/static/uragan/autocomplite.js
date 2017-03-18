/**
 * Created by koshelev on 14.06.15.
 */

$geoobject = $('#div_id_title');

function geocode(term, options) {
  var n_opt = {q: term, format: 'json', polygon_kml: 1},
    geocode_data = [];


  $.getJSON("http://nominatim.openstreetmap.org/search", n_opt, function (data, status) {
    if (status === 'success') {
      $geoobject.data('nominatim', data.map(function (item) {
          return {
            value: item.display_name,
            data: {
              coder: 'Nominatim',
              id: '(' + item.lat + ', ' + item.lon + ')',
              lat: item.lat,
              lon: item.lon,
              polygon: item.geokml
            }
          }
        })
      );
    }
    else {
      $geoobject.data('nominatim', {value: 'Not found =(', data: {coder: 'nominatim'}})
    }
  });

  geocoder.geocode({'address': term}, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      $geoobject.data(
        'google', results.map(function (obj) {
          return {
            value: obj.formatted_address,
            data: {
              coder: 'Google',
              id: '(' + obj.geometry.location.lat() + ', ' + obj.geometry.location.lng() + ')',
              lat: obj.geometry.location.lat(),
              lon: obj.geometry.location.lng(),
              polygon: ''
            }
          };
        })
      );
    }
    else {
      $geoobject.data('google', {value: 'Not found =(', data: {coder: 'google'}})
    }
  });
  var g = $geoobject.data().google,
    n = $geoobject.data().nominatim;
  return g.concat(n);
}


$('#id_title').devbridgeAutocomplete({
  //serviceUrl: 'http://nominatim.openstreetmap.org/search',
  minChars: 3,
  lookup: function (query, done) {
    // Do ajax call or lookup locally, when done,
    // call the callback and pass your results:
    var result = {suggestions: geocode(query)};
    console.log(query, result.suggestions);
    done(result);
  },
  onSelect: function (suggestion) {
    $("#id_lat").val(suggestion.data.lat);
    $("#id_lon").val(suggestion.data.lon);
    $("#id_title").val(suggestion.value);
    $('#id_polygon').val(suggestion.data.polygon);
    var location = new google.maps.LatLng(suggestion.data.lat, suggestion.data.lon);
    kml_parser.parseKmlString('<kml>' + suggestion.data.polygon + '</kml>');
    marker.setPosition(location);
    map.setCenter(location);
    alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
  },
  groupBy: 'coder'
});
