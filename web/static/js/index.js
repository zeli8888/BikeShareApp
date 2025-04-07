/**
 * Import necessary functions from other modules.
 */
import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./userLocation.js";
import { getStationRoute } from "./route.js"
import { showWeatherInfoContainer, toggleSidebarContent } from "./sidebar.js";
import { getCurrentBikes } from "./stations.js";
import { getCurrentWeather } from "./weather.js";

/**
 * Set up event listener for share location button.
 */
const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

/**
 * Expose functions to the global scope.
 */
window.showWeatherInfoContainer = showWeatherInfoContainer;
window.toggleSidebarContent = toggleSidebarContent;
window.getStationRoute = getStationRoute;
window.getCurrentBikes = getCurrentBikes;
window.getCurrentWeather = getCurrentWeather;

/**
 * Initialize user location from session storage or default value.
 */
const storedLocation = sessionStorage.getItem('userLocation');
if (storedLocation && storedLocation !== 'undefined') {
    window.coords = JSON.parse(storedLocation);
} else {
    window.coords = {
        latitude: 53.3498,
        longitude: -6.2603
    }
}

/**
 * Show weather info container.
 */
showWeatherInfoContainer();

/**
 * Initialize map.
 */
window.initMap = initMap;
loadGoogleMapsApi();