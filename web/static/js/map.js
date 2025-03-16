import { addStationMarker } from "./stations.js";
import { addPlaceControls } from "./route.js";
function initMap() {
    const location = {
        lat: window.coords.latitude,
        lng: window.coords.longitude
    };
    let map = new google.maps.Map(document.getElementById("map"), {
        mapId: window.GOOGLE_MAP_ID,
        center: location,
        zoom: 13,
    });

    window.googleMap = map;
    addPlaceControls();
    addStationMarker(window.BIKES_URL);
}

function loadGoogleMapsApi() {
    const googleMapScript = document.createElement('script');
    googleMapScript.src = "https://maps.googleapis.com/maps/api/js?key=" + window.GOOGLE_MAP_KEY + "&callback=initMap&libraries=marker,places&loading=async";
    googleMapScript.async = true;
    document.body.appendChild(googleMapScript);
}

export { loadGoogleMapsApi, initMap }