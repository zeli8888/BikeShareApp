import { getWeather } from './weather.js';
import { renderBikeTrendChart } from "./bikeTrend.js";
import { renderBikePredictionChart } from './prediction.js';

function showWeatherInfoContainer() {
    getWeather(window.WEATHER_URL, window.coords.latitude, window.coords.longitude);
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
    document.getElementById('sidebar-return').style.display = 'none';
}

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

function showRouteContainer() {
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'none';
    document.getElementById('route-container').style.display = 'block';
    if (document.getElementById('sidebar-toggle').textContent === 'Hide') {
        document.getElementById('sidebar-return').style.display = 'block';
    }
}

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