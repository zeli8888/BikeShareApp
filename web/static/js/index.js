import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./user_location.js";
import { calculateAndDisplayRoute, getStationRoute } from "./route.js"
import { show_weather_info_container, toggle_sidebar_content } from "./sidebar.js";

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.show_weather_info_container = show_weather_info_container;
window.toggle_sidebar_content = toggle_sidebar_content;
window.calculateAndDisplayRoute = calculateAndDisplayRoute;
window.getStationRoute = getStationRoute;

document.getElementById("travel-mode").addEventListener("change", () => {
    calculateAndDisplayRoute(window.target_lat, window.target_lng, document.getElementById("travel-mode").value, window.start_lat, window.start_lng);
});

const storedLocation = sessionStorage.getItem('userLocation');
if (storedLocation && storedLocation !== 'undefined') {
    window.coords = JSON.parse(storedLocation);
} else {
    window.coords = {
        latitude: 53.3498,
        longitude: -6.2603
    }
}
show_weather_info_container();

window.initMap = initMap;
loadGoogleMapsApi();