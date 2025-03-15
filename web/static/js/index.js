import { getWeather } from "./weather.js";
import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./user_location.js";
import { calculateAndDisplayRoute } from "./route.js"
import { show_weather_info, show_station_info_container } from "./sidebar.js";

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.show_weather_info = show_weather_info;
window.show_station_info_container = show_station_info_container;
window.calculateAndDisplayRoute = calculateAndDisplayRoute;

document.getElementById("travel-mode").addEventListener("change", () => {
    calculateAndDisplayRoute(window.target.lat, window.target.lng, document.getElementById("travel-mode").value);
});

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