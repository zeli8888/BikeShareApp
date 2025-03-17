import { getWeather } from './weather.js';
function show_weather_info_container() {
    getWeather(window.WEATHER_URL, window.coords.latitude, window.coords.longitude);
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
    document.getElementById('sidebar-return').style.display = 'none';
}

function show_station_info_container() {
    document.getElementById('station-info-container').style.display = 'block';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
    if (document.getElementById('sidebar-toggle').textContent === 'Hide') {
        document.getElementById('sidebar-return').style.display = 'block';
    }
}

function show_route_container() {
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'none';
    document.getElementById('route-container').style.display = 'block';
    if (document.getElementById('sidebar-toggle').textContent === 'Hide') {
        document.getElementById('sidebar-return').style.display = 'block';
    }
}

function toggle_sidebar_content() {
    const toggle_button = document.getElementById('sidebar-toggle');
    if (toggle_button.textContent === 'Hide') {
        toggle_button.textContent = 'Show';
        document.getElementById('sidebar-content').style.display = 'none';
        document.getElementById('sidebar-return').style.display = 'none';
    } else {
        toggle_button.textContent = 'Hide';
        document.getElementById('sidebar-content').style.display = 'block';
        if (document.getElementById('route-container').style.display === 'block' || document.getElementById('station-info-container').style.display === 'block') {
            document.getElementById('sidebar-return').style.display = 'block';
        }
    }
}

export { show_weather_info_container, show_station_info_container, show_route_container, toggle_sidebar_content };