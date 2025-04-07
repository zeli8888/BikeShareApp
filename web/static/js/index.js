import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./userLocation.js";
import { calculateAndDisplayRoute, getStationRoute } from "./route.js"
import { showWeatherInfoContainer, toggleSidebarContent } from "./sidebar.js";
import { getCurrentBikes } from "./stations.js";
import { getCurrentWeather } from "./weather.js";

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.showWeatherInfoContainer = showWeatherInfoContainer;
window.toggleSidebarContent = toggleSidebarContent;
window.calculateAndDisplayRoute = calculateAndDisplayRoute;
window.getStationRoute = getStationRoute;
window.getCurrentBikes = getCurrentBikes;
window.getCurrentWeather = getCurrentWeather;

document.getElementById("travel-mode").addEventListener("change", () => {
    calculateAndDisplayRoute(window.targetLat, window.targetLng, document.getElementById("travel-mode").value, window.startLat, window.startLng);
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
showWeatherInfoContainer();

window.initMap = initMap;
loadGoogleMapsApi();