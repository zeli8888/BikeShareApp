import { show_route } from "./sidebar.js";
function initDirectionsService() {
    window.directionsRenderer = new google.maps.DirectionsRenderer();
    window.directionsService = new google.maps.DirectionsService();
    window.directionsRenderer.setMap(window.googleMap);
    window.directionsRenderer.setPanel(document.getElementById("route"));
}

function calculateAndDisplayRoute(end_lat, end_lng, selectedMode) {
    if (!window.directionsService) {
        initDirectionsService();
    }
    document.getElementById("travel-mode").value = selectedMode;
    document.getElementById('google-map-link').innerHTML =
        `<br>
    <a href="https://www.google.com/maps/dir/?api=1&destination=${end_lat},${end_lng}&mode=${selectedMode}" target="_blank">Open Google Map</a>
    `
    show_route();

    window.directionsService
        .route({
            origin: window.coords ? new google.maps.LatLng(window.coords.latitude, window.coords.longitude) : new google.maps.LatLng(53.3498, -6.2603),
            destination: new google.maps.LatLng(end_lat, end_lng),
            travelMode: google.maps.TravelMode[selectedMode],
        })
        .then((response) => {
            window.directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + e.status));
    window.target = { lat: end_lat, lng: end_lng };
}

export { calculateAndDisplayRoute }