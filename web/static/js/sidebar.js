import { getWeather } from './weather.js';
import { renderBikeTrendChart } from "./bikeTrend.js";
import { renderBikePredictionChart } from './prediction.js';

/**
 * Shows the weather info container and hides the other containers.
 * Retrieves the current weather data for the user's location from the backend
 * and displays it in the weather info container.
 */
function showWeatherInfoContainer() {
    getWeather(window.WEATHER_URL, window.coords.latitude, window.coords.longitude);
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
    document.getElementById('sidebar-return').style.display = 'none';
}

/**
 * Shows the station info container and the weather info container, and hides the route container.
 * If the sidebar is visible, also shows the 'Return' button and renders the bike prediction and trend charts.
 */
function showStationInfoContainer() {
    document.getElementById('station-info-container').style.display = 'block';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
    if (document.getElementById('sidebar-toggle').textContent === 'Hide') {
        document.getElementById('sidebar-return').style.display = 'block';
        // when the sidebar is hidden, the chart cannot be rendered 
        // because the container width is 0, so only show when it is visible
        renderBikePredictionChart();
        renderBikeTrendChart();
    }
}

/**
 * Shows the route container and hides the other containers.
 * If the sidebar is visible, also shows the 'Return' button.
 */

function showRouteContainer() {
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'none';
    document.getElementById('route-container').style.display = 'block';
    if (document.getElementById('sidebar-toggle').textContent === 'Hide') {
        document.getElementById('sidebar-return').style.display = 'block';
    }
}

/**
 * Toggles the visibility of the sidebar content and the 'Return' button.
 * If the station info container or route container is visible, the 'Return' button is also visible,
 * and the bike prediction and trend charts are rendered if the station info container is visible.
 */
function toggleSidebarContent() {
    const toggle_button = document.getElementById('sidebar-toggle');
    if (toggle_button.textContent === 'Hide') {
        toggle_button.textContent = 'Show';
        document.getElementById('sidebar-content').style.display = 'none';
        document.getElementById('sidebar-return').style.display = 'none';
    } else {
        toggle_button.textContent = 'Hide';
        document.getElementById('sidebar-content').style.display = 'block';
        if (document.getElementById('station-info-container').style.display === 'block') {
            document.getElementById('sidebar-return').style.display = 'block';
            renderBikePredictionChart();
            renderBikeTrendChart();
        } else if (document.getElementById('route-container').style.display === 'block') {
            document.getElementById('sidebar-return').style.display = 'block';
        }
    }
}

export { showWeatherInfoContainer, showStationInfoContainer, showRouteContainer, toggleSidebarContent };