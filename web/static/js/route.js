import { show_route_container } from "./sidebar.js";
function initDirectionsService() {
    window.directionsRenderer = new google.maps.DirectionsRenderer();
    window.directionsService = new google.maps.DirectionsService();
    window.directionsRenderer.setMap(window.googleMap);
    window.directionsRenderer.setPanel(document.getElementById("route"));
}

function calculateAndDisplayRoute(end_lat, end_lng, selectedMode, start_lat = null, start_lng = null) {
    if (!window.directionsService) {
        initDirectionsService();
    }
    if (start_lat == null || start_lng == null) {
        start_lat = window.coords.latitude;
        start_lng = window.coords.longitude;
    }
    document.getElementById('google-map-link').innerHTML = `<br>
    <a href="https://www.google.com/maps/dir/?api=1&origin=${start_lat},${start_lng}&destination=${end_lat},${end_lng}&mode=${selectedMode}" target="_blank">Open Google Map</a>
    `
    show_route_container();

    window.directionsService
        .route({
            origin: new google.maps.LatLng(start_lat, start_lng),
            destination: new google.maps.LatLng(end_lat, end_lng),
            travelMode: google.maps.TravelMode[selectedMode],
        })
        .then((response) => {
            window.directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + e.status));
    window.target_lat = end_lat;
    window.target_lng = end_lng;
    window.start_lat = start_lat;
    window.start_lng = start_lng;
}

function getStationRoute(lat, lng) {
    calculateAndDisplayRoute(lat, lng, document.getElementById('travel-mode').value);
}

function addPlaceControls() {
    const des = document.getElementById("des-input");
    window.googleMap.controls[google.maps.ControlPosition.TOP_LEFT].push(des);
    const des_autocomplete = new google.maps.places.Autocomplete(des, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    des_autocomplete.bindTo("bounds", window.googleMap);

    des_autocomplete.addListener("place_changed", () => {

        const place = des_autocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
            return;
        }
        calculateAndDisplayRoute(place.geometry.location.lat(), place.geometry.location.lng(), document.getElementById("travel-mode").value);
    });

    const start = document.getElementById("start-input");
    const start_autocomplete = new google.maps.places.Autocomplete(start, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    start_autocomplete.bindTo("bounds", window.googleMap);

    start_autocomplete.addListener("place_changed", () => {

        const place = start_autocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
            return;
        }
        calculateAndDisplayRoute(window.target_lat, window.target_lng, document.getElementById("travel-mode").value, place.geometry.location.lat(), place.geometry.location.lng());
    });
}

export { calculateAndDisplayRoute, addPlaceControls, getStationRoute }