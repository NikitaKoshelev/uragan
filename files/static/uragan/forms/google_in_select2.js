/**
 * Created by koshelev on 14.06.15.
 */

var $google_geocode = $('<select class="form-control" id="google_geocode" style="width: 100%"></select>');
//    $google_geocode.select2({
//        placeholder: gettext('Search geo object with Google Geocoder...'),
//        allowClear: true,
//
//        ajax: {
//            url: "https://maps.googleapis.com/maps/api/geocode/json",
//            dataType: 'json',
//            type: "GET",
//            cache: true,
//            data: function (params, page) {
//                return {
//                    address: params.term, // search term
//                    key: 'AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw'
//                };
//            },
//            processResults: function (data, params) {
//                // parse the results into the format expected by Select2.
//                // since we are using custom formatting functions we do not need to
//                // alter the remote JSON data
//
//                params.page = params.page || 1;
//
//                // If your ajax response doesn't have id and text attributes you should fix them client side
//
//                var select2data = data.results.map(function (obj) {
//                    return {
//                        id: '(' + obj.geometry.location.lat + ', ' + obj.geometry.location.lng + ')',
//                        text: obj.formatted_address,
//                        lat: obj.geometry.location.lat,
//                        lon: obj.geometry.location.lng,
//                        polygon: ''
//                    };
//                });
//
//                return {
//                    results: select2data
//                };
//            }
//        },
//
//        templateResult: function (google_geocode) {
//            if (google_geocode.loading) {
//                return google_geocode.text;
//            }
//            else {
//                return $('<strong>{0}</strong><span class="pull-right">({1},{2})</span>'
//                        .f(google_geocode.text, google_geocode.lat, google_geocode.lon)
//                );
//            }
//
//        } // omitted for brevity, see the source of this page
//
//        //templateSelection: function (google_geocode) {
//        //    return google_geocode.display_name;
//        //} // omitted for brevity, see the source of this page
//    });
//});

var options = {
  placeholder: gettext('Search geo object with Google Geocoder...'),
  allowClear: true,
  templateResult: function (google_geocode) {
    if (google_geocode.loading) {
      return google_geocode.text;
    }
    else {
      return $('<strong>{0}</strong><span class="pull-right">({1},{2})</span>'
        .f(google_geocode.text, google_geocode.lat, google_geocode.lon)
      );
    }
  },
  query: function (query) {


    // here we check whether the user has entered some search term
    // and enforce a min term length to 2 chars
    if (query.term && query.term.length > 2) {
      var data = {results: []};
      //$.getJSON({
      //    url: "https://maps.googleapis.com/maps/api/geocode/json",
      //    data: {address: query.term, key: 'AIzaSyDVEXypca7bWLD1my4Wvc6AQTjsIM88MZw'},
      //    success: function (data) {
      //        console.log(data);
      //        var select2data = data.results.map(function (obj) {
      //            return {
      //                id: '(' + obj.geometry.location.lat + ', ' + obj.geometry.location.lng + ')',
      //                text: obj.formatted_address,
      //                lat: obj.geometry.location.lat,
      //                lon: obj.geometry.location.lng,
      //                polygon: ''
      //            };
      //        });
      //    }
      //});
      // data from server is something like
      // {"Locations":[{"text":"Country","children":[{"id":11107,"text":"UNITED KINGDOM (GB)"}]}]}
      $.when(google_geocoder(query.term)).then(function () {
        if (data) {
          console.log(data);
          //query.callback({results: {text: 'Google', children: g}});
        }
      })
    }
    else
      query.callback(); // no search term, display default data
  }
};

$(document).ready(function () {
  $google_geocode.select2(options);
});


$('#geocoders')
  .append($('<div>', {class: 'col-md-6 form-group'})
    .append($('<label>', {for: "google_geocode", class: "control-label"})
        .append('Google geocoder'),
      $google_geocode)
  );


$google_geocode.on('select2:select', function (e) {
  var google_geocode = e.params.data;
  $("[id^=id_][id$=lat]").val(google_geocode.lat);
  $("[id^=id_][id$=lon]").val(google_geocode.lon);
  $("[id^=id_][id$=title]").val(google_geocode.text);
  $("[id^=id_][id$=polygon]").val(google_geocode.polygon);
  var location = new google.maps.LatLng(google_geocode.lat, google_geocode.lon);
  marker.setPosition(location);
  map.setCenter(location);

});


function google_geocoder(term) {
  return geocoder.geocode({'address': term}, function (results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        data.results.push(results.map(function (obj) {
            return {
              id: '(' + obj.geometry.location.lat + ', ' + obj.geometry.location.lng + ')',
              text: obj.formatted_address,
              lat: obj.geometry.location.lat,
              lon: obj.geometry.location.lng,
              polygon: ''
            };
          })
        );
        //data.results = [{text: 'Google Geocode', children: g }];
        //showMessage(false, gettext('Was found geo object') + ': "{0}"'.f(title.bold().italics()));
      }
    }
  });
}
