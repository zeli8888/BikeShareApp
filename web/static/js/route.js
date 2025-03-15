function initDirectionsService() {
    window.directionsRenderer = new google.maps.DirectionsRenderer();
    window.directionsService = new google.maps.DirectionsService();
    window.directionsRenderer.setMap(window.googleMap);
    window.directionsRenderer.setPanel(document.getElementById("sidebar"));
}

function calculateAndDisplayRoute(end_lat, end_lng, selectedMode) {
    if (!window.directionsService) {
        initDirectionsService();
    }
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
}

export { calculateAndDisplayRoute }