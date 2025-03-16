import { getWeather } from './weather.js';
function show_weather_info_container() {
    getWeather(window.WEATHER_URL, window.coords.latitude, window.coords.longitude);
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
}

function show_station_info_container() {
    document.getElementById('station-info-container').style.display = 'block';
    document.getElementById('weather-info-container').style.display = 'block';
    document.getElementById('route-container').style.display = 'none';
}

function show_route_container() {
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('weather-info-container').style.display = 'none';
    document.getElementById('route-container').style.display = 'block';
}

export { show_weather_info_container, show_station_info_container, show_route_container };