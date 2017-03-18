/**
 * Created by koshelev on 14.06.15.
 */

var $nominatim_geocode = $('<select class="form-control" id="nominatim_geocode"></select>');
$(document).ready(function () {
  $nominatim_geocode.select2({
    placeholder: gettext('Search geo object with Nominatim Geocoder...'),
    allowClear: true,
    minimumInputLength: 3,
    language: "ru",
    width: '100%',

    ajax: {
      url: "http://nominatim.openstreetmap.org/search",
      dataType: 'json',
      delay: 1000,
      type: "GET",
      cache: true,
      async: false,
      data: function (params, page) {
        return {
          q: params.term, // search term
          format: 'json'
          // page: page || 1
        };
      },
      processResults: function (data, params) {
        // parse the results into the format expected by Select2.
        // since we are using custom formatting functions we do not need to
        // alter the remote JSON data

        params.page = params.page || 1;

        // If your ajax response doesn't have id and text attributes you should fix them client side
        var select2data = data.map(function (obj) {
          return {
            id: '(' + obj.lat + ', ' + obj.lon + ')',
            text: obj.display_name,
            lat: obj.lat,
            lon: obj.lon
          };
        });

        return {
          results: select2data
        };
      }
    },

    templateResult: function (nominatim_geocode) {
      if (nominatim_geocode.loading) {
        //window.alert(nominatim_geocode.text);
        return nominatim_geocode.text;
      }
      else {
        return $('<strong>{0}</strong><span class="pull-right">({1},{2})</span>'
          .f(nominatim_geocode.text, nominatim_geocode.lat, nominatim_geocode.lon)
        );
        //return $('<div class="row">' +
        //    '  <div class="col-md-9">' + nominatim_geocode.text + '</div>' +
        //   '  <div class="col-md-3">(' + nominatim_geocode.lat + ', ' + nominatim_geocode.lon + ')</div>' +
        //    '</div>');
      }

    } // omitted for brevity, see the source of this page

    //templateSelection: function (nominatim_geocode) {
    //    return nominatim_geocode.display_name;
    //} // omitted for brevity, see the source of this page
  });
});

$('#geocoders')
  .append($('<div>', {class: 'col-md-6 form-group'})
    .append($('<label>', {for: "nominatim_geocode", class: "control-label"})
        .append('Nominatim geocoder'),
      $nominatim_geocode)
  );

$nominatim_geocode.on('select2:select', function (e) {
  var nominatim_geocode = e.params.data;
  $("[id^=id_][id$=lat]").val(nominatim_geocode.lat);
  $("[id^=id_][id$=lon]").val(nominatim_geocode.lon);
  $("[id^=id_][id$=title]").val(nominatim_geocode.text);
  var location = new google.maps.LatLng(nominatim_geocode.lat, nominatim_geocode.lon);
  marker.setPosition(location);
  map.setCenter(location);

});
