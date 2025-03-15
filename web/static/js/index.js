import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./user_location.js";
import { calculateAndDisplayRoute } from "./route.js"
import { show_weather_info_container, show_station_info_container } from "./sidebar.js";

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.show_weather_info_container = show_weather_info_container;
window.show_station_info_container = show_station_info_container;
window.calculateAndDisplayRoute = calculateAndDisplayRoute;

document.getElementById("travel-mode").addEventListener("change", () => {
    calculateAndDisplayRoute(window.target.lat, window.target.lng, document.getElementById("travel-mode").value);
});

const storedLocation = sessionStorage.getItem('userLocation');
if (storedLocation && storedLocation !== 'undefined') {
    window.coords = JSON.parse(storedLocation);
}
show_weather_info_container();

window.initMap = initMap;
loadGoogleMapsApi();