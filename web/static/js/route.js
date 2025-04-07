import { showRouteContainer } from "./sidebar.js";
/**
 * Initializes the Google Maps DirectionsService and DirectionsRenderer objects.
 * Set up event listener for travel mode change.
 */
function initDirectionsService() {
    window.directionsRenderer = new google.maps.DirectionsRenderer();
    window.directionsService = new google.maps.DirectionsService();
    window.directionsRenderer.setMap(window.googleMap);
    window.directionsRenderer.setPanel(document.getElementById("route"));

    document.getElementById("travel-mode").addEventListener("change", () => {
        calculateAndDisplayRoute(window.targetLat, window.targetLng, document.getElementById("travel-mode").value, window.startLat, window.startLng);
    });

}

/**
 * Calculates the route from start coordinates to the end coordinates and
 * displays it on the map.
 *
 * If no start coordinates are provided, the user's current location is used as the
 * starting point.
 *
 * The route is displayed using the Google Maps DirectionsRenderer, and a link to
 * Google Maps is also displayed allowing the user to view the route in Google Maps.
 *
 * @param {number} endLat - The latitude of the destination.
 * @param {number} endLng - The longitude of the destination.
 * @param {string} selectedMode - The mode of transportation to use for the route.
 * @param {number} [startLat] - The latitude of the starting point.
 * @param {number} [startLng] - The longitude of the starting point.
 */
function calculateAndDisplayRoute(endLat, endLng, selectedMode, startLat = null, startLng = null) {
    if (!window.directionsService) {
        initDirectionsService();
    }
    if (startLat == null || startLng == null) {
        startLat = window.coords.latitude;
        startLng = window.coords.longitude;
    }
    /**
     * Update the Google Map link.
     */
    document.getElementById('google-map-link').innerHTML = `<br>
    <a href="https://www.google.com/maps/dir/?api=1&origin=${startLat},${startLng}&destination=${endLat},${endLng}&mode=${selectedMode}" target="_blank">🗺️ Open Google Map</a>
    `

    /**
     * Show the route container.
     */
    showRouteContainer();

    /**
     * Calculate the route using the DirectionsService.
     */
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

    /**
     * Store the target and start coordinates for handling the start, destination and travel model change events.
     */
    window.targetLat = endLat;
    window.targetLng = endLng;
    window.startLat = startLat;
    window.startLng = startLng;
}

/**
 * Calculate the route from user's current location to the station with the
 * coordinates (lat, lng) and show the route on the map.
 * Used in stations.js for each marker.
 *
 * @param {number} lat The latitude of the station.
 * @param {number} lng The longitude of the station.
 */
function getStationRoute(lat, lng) {
    calculateAndDisplayRoute(lat, lng, document.getElementById('travel-mode').value);
}

/**
 * Adds input fields for the start and destination of a route to the map.
 *
 * The input fields are added as a custom control to the map, and are
 * positioned at the top left of the map. For mobile phones, the input fields
 * are positioned at the left top of the map.
 *
 * Each input field has an autocomplete feature that is bound to the map's
 * bounds. When a user selects a place from the autocomplete dropdown, the
 * calculateAndDisplayRoute function is called with the latitude and longitude
 * of the selected place.
 */
function addPlaceControls() {
    /**
     * Get the destination input element.
     * @type {HTMLInputElement}
     */
    const des = document.getElementById("des-input");

    /**
     * Get the screen width.
     * @type {number}
     */
    var screenWidth = window.innerWidth;

    /**
     * Add the destination input to the map controls.
     */
    if (screenWidth < 800) { // mobile phones
        window.googleMap.controls[google.maps.ControlPosition.LEFT_TOP].push(des);
    } else {
        window.googleMap.controls[google.maps.ControlPosition.TOP_LEFT].push(des);
    }

    /**
     * Create a new Autocomplete instance for the destination input.
     * @type {google.maps.places.Autocomplete}
     */
    const desAutocomplete = new google.maps.places.Autocomplete(des, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    /**
     * Bind the Autocomplete to the map bounds.
     */
    desAutocomplete.bindTo("bounds", window.googleMap);

    /**
     * Add a listener for the place changed event.
     */
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

export { addPlaceControls, getStationRoute }