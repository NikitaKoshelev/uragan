/**
 * Created by NikitaKoshelev on 25.06.2015.
 */

$('#map_canvas').css('height', '600px').css('background', 'inherit');//$('.content').css('height'));

function initialize() {
  console.log(lon, lat);
  var location = new google.maps.LatLng(lat, lon),
    map = new google.maps.Map(document.getElementById("map_canvas"), {
      center: location,
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.HYBRID
    }),
    marker = new google.maps.Marker({map: map, position: location}),
    kml = new google.maps.KmlLayer({
      url: window.location.href.split('#')[0] + '?get_kml=true',
      map: map
    });
}

$(document).ready(asyncGmapsInitialization());
