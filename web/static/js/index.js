import { getWeather } from "./weather.js";
import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./user_location.js";
import { calculateAndDisplayRoute } from "./route.js"

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.calculateAndDisplayRoute = calculateAndDisplayRoute;

const storedLocation = sessionStorage.getItem('userLocation');
if (storedLocation && storedLocation !== 'undefined') {
    window.coords = JSON.parse(storedLocation);
}

if (window.coords) {
    getWeather(window.WEATHER_URL + `?latitude=${window.coords.latitude}&longitude=${window.coords.longitude}`);
} else {
    getWeather(window.WEATHER_URL);
}

window.initMap = initMap;
loadGoogleMapsApi();