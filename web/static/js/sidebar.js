function show_weather_info() {
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('route').style.display = 'none';
    document.getElementById('weather-info').style.display = 'block';
}

function show_station_info_container() {
    document.getElementById('weather-info').style.display = 'none';
    document.getElementById('route').style.display = 'none';
    document.getElementById('station-info-container').style.display = 'block';
}

function show_route() {
    document.getElementById('weather-info').style.display = 'none';
    document.getElementById('station-info-container').style.display = 'none';
    document.getElementById('route').style.display = 'block';
}

export { show_weather_info, show_station_info_container, show_route };