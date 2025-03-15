import { addStationMarker } from "./stations.js";
function initMap() {
    const location = window.coords ? {
        lat: window.coords.latitude,
        lng: window.coords.longitude
    } :
        {
            // The location of Dublin City Center
            lat: 53.3498,
            lng: -6.2603
        }
        ;
    let map = new google.maps.Map(document.getElementById("map"), {
        mapId: window.GOOGLE_MAP_ID,
        center: location,
        zoom: 13,
    });

    window.googleMap = map;
    addStationMarker(window.BIKES_URL);
}

function loadGoogleMapsApi() {
    const googleMapScript = document.createElement('script');
    googleMapScript.src = "https://maps.googleapis.com/maps/api/js?key=" + window.GOOGLE_MAP_KEY + "&callback=initMap&libraries=marker&loading=async";
    googleMapScript.async = true;
    document.body.appendChild(googleMapScript);
}

export { loadGoogleMapsApi, initMap }