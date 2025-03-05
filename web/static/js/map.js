import { addStationMarker } from "./stations.js";
import { getWeather } from "./weather.js";
function initMap() {
    // The location of Dublin
    const location = {
        lat: 53.3498,
        lng: -6.2603
    };
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

getWeather(window.WEATHER_URL);
window.initMap = initMap;
loadGoogleMapsApi();

export { loadGoogleMapsApi, initMap }