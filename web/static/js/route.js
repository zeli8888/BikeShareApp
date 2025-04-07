import { showRouteContainer } from "./sidebar.js";
function initDirectionsService() {
    window.directionsRenderer = new google.maps.DirectionsRenderer();
    window.directionsService = new google.maps.DirectionsService();
    window.directionsRenderer.setMap(window.googleMap);
    window.directionsRenderer.setPanel(document.getElementById("route"));
}

function calculateAndDisplayRoute(endLat, endLng, selectedMode, startLat = null, startLng = null) {
    if (!window.directionsService) {
        initDirectionsService();
    }
    if (startLat == null || startLng == null) {
        startLat = window.coords.latitude;
        startLng = window.coords.longitude;
    }
    document.getElementById('google-map-link').innerHTML = `<br>
    <a href="https://www.google.com/maps/dir/?api=1&origin=${startLat},${startLng}&destination=${endLat},${endLng}&mode=${selectedMode}" target="_blank">🗺️ Open Google Map</a>
    `
    showRouteContainer();

    window.directionsService
        .route({
            origin: new google.maps.LatLng(startLat, startLng),
            destination: new google.maps.LatLng(endLat, endLng),
            travelMode: google.maps.TravelMode[selectedMode],
        })
        .then((response) => {
            window.directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed, Please try again"));
    window.targetLat = endLat;
    window.targetLng = endLng;
    window.startLat = startLat;
    window.startLng = startLng;
}

function getStationRoute(lat, lng) {
    calculateAndDisplayRoute(lat, lng, document.getElementById('travel-mode').value);
}

function addPlaceControls() {
    const des = document.getElementById("des-input");
    var screenWidth = window.innerWidth;
    if (screenWidth < 800) { // mobile phones
        window.googleMap.controls[google.maps.ControlPosition.LEFT_TOP].push(des);
    } else {
        window.googleMap.controls[google.maps.ControlPosition.TOP_LEFT].push(des);
    }
    const desAutocomplete = new google.maps.places.Autocomplete(des, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    desAutocomplete.bindTo("bounds", window.googleMap);

    desAutocomplete.addListener("place_changed", () => {

        const place = desAutocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
            return;
        }
        calculateAndDisplayRoute(place.geometry.location.lat(), place.geometry.location.lng(), document.getElementById("travel-mode").value);
    });

    const start = document.getElementById("start-input");
    const startAutocomplete = new google.maps.places.Autocomplete(start, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    startAutocomplete.bindTo("bounds", window.googleMap);

    startAutocomplete.addListener("place_changed", () => {

        const place = startAutocomplete.getPlace();
        if (!place.geometry || !place.geometry.location) {
            return;
        }
        calculateAndDisplayRoute(window.targetLat, window.targetLng, document.getElementById("travel-mode").value, place.geometry.location.lat(), place.geometry.location.lng());
    });
}

export { calculateAndDisplayRoute, addPlaceControls, getStationRoute }