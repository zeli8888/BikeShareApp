import { addStationMarker } from "./stations.js";
import { addPlaceControls } from "./route.js";
/**
 * Initializes the map on the page, using the user's location as the center.
 *
 * The map is configured with a compact map type control in the top left
 * corner of the map. The sidebar is added to the map as a custom control in
 * the top right corner.
 *
 * A place autocomplete control is added to the map, which is used to update
 * the selected destination.
 *
 * Station markers are loaded from the backend URL and added to the map.
 */
function initMap() {
    const location = {
        lat: window.coords.latitude,
        lng: window.coords.longitude
    };
    let map = new google.maps.Map(document.getElementById("map"), {
        mapId: window.GOOGLE_MAP_ID,
        center: location,
        zoom: 13,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.COMPACT,
            position: google.maps.ControlPosition.TOP_LEFT
        }
    });

    window.googleMap = map;
    addPlaceControls();
    addStationMarker(window.BIKES_URL);

    window.googleMap.controls[google.maps.ControlPosition.TOP_RIGHT].push(document.getElementById("sidebar"));
}

/**
 * Loads the Google Maps API by adding a script tag to the document body.
 *
 * The API key is taken from the window.GOOGLE_MAP_KEY variable.
 *
 * The libraries marker, places, and visualization are loaded, and the
 * callback function set to initMap.
 *
 * The loading parameter is set to async, so that the script does not
 * block the page load.
 */
function loadGoogleMapsApi() {
    const googleMapScript = document.createElement('script');
    googleMapScript.src = "https://maps.googleapis.com/maps/api/js?key=" + window.GOOGLE_MAP_KEY + "&callback=initMap&libraries=marker,places,visualization&loading=async";
    googleMapScript.async = true;
    document.body.appendChild(googleMapScript);
}

export { loadGoogleMapsApi, initMap }