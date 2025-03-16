import { show_station_info_container } from "./sidebar.js";
import { getWeather } from "./weather.js";
async function addStationMarker(bikesUrl) {
    const map = window.googleMap;
    const { stations, availabilities } = await fetch(bikesUrl).then(response => response.json());
    window.markers = {};

    // Create AdvancedMarkerElement For User Location
    const user_location_marker_img = document.createElement('img');
    user_location_marker_img.src = "https://maps.google.com/mapfiles/ms/micons/yellow-dot.png";
    window.user_location_marker = new google.maps.marker.AdvancedMarkerElement({
        position: new google.maps.LatLng(window.coords.latitude, window.coords.longitude),
        map: map,
        content: user_location_marker_img,
        title: 'YOUR LOCATION'
    });

    const station_marker_img = document.createElement('img');
    station_marker_img.src = "https://maps.google.com/mapfiles/ms/micons/red-dot.png";
    stations.forEach(station => {
        const { address, banking, bike_stands, name, number, position_lat, position_lng } = station;
        const marker_img = station_marker_img.cloneNode(true);
        // Create AdvancedMarkerElement
        const marker = new google.maps.marker.AdvancedMarkerElement({
            position: new google.maps.LatLng(position_lat, position_lng),
            map: map,
            content: marker_img,
            title: name,  // Tooltip for marker
            ariaLabel: name // Accessible name for screen readers
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `
              <div class="info-window-content">
                <span class="info-window-title"><strong>${name}</strong></span><br>
                <a href="#" onclick="getStationRoute(${position_lat}, ${position_lng})">➡️Directions<br></a>
                <!-- Banking: ${banking}<br> -->
                <!-- Bike Stands: ${bike_stands}<br> -->
              </div>
            `
        });

        marker.addListener("gmp-click", () => {
            infoWindow.open(map, marker);
            document.getElementById('station-info').innerHTML = infoWindow.content;
            getWeather(window.WEATHER_URL, position_lat, position_lng);
            show_station_info_container();
        });

        marker.infoWindow = infoWindow;
        window.markers[number] = marker;
    });

    const heatmapBikesData = [];
    const heatmapStandsData = [];
    availabilities.forEach(availability => {
        const { available_bike_stands, available_bikes, last_update, number, status } = availability;
        const infoWindow = window.markers[number].infoWindow;
        infoWindow.setContent(infoWindow.content + `
            <div class="info-window-content">
                Available Bikes 🚲: ${available_bikes}<br>
                Available Stands 🅿️: ${available_bike_stands}<br>
                Status: ${status}<br>
                Last Update: ${new Date(last_update).toLocaleTimeString()}
            </div >
        `);
        const location = new window.google.maps.LatLng(window.markers[number].position.lat, window.markers[number].position.lng);
        heatmapBikesData.push({
            location: location,
            weight: available_bikes
        });
        heatmapStandsData.push({
            location: location,
            weight: available_bike_stands
        });
    });
    window.heatmapBikes = new google.maps.visualization.HeatmapLayer({
        data: heatmapBikesData,
        radius: 25,
        map: window.googleMap
    });
    window.heatmapStands = new google.maps.visualization.HeatmapLayer({
        data: heatmapStandsData,
        radius: 25,
        map: null
    });

    addLegend();
    addRadioButtons();
}

function addLegend() {
    const legend = document.createElement('div');
    legend.id = 'heatmapLegend';
    legend.innerHTML = `
    <div id="heatmapLegend-title" class="legend-title">Available Bikes</div>
    <div class="legend-gradient"></div>
    <div class="legend-labels">
        <span>0</span>
        <span>10</span>
        <span>20</span>
        <span>30</span>
        <span>40</span>
        <span>50+</span>
    </div>
    `;

    const mapContainer = document.getElementById('map');
    mapContainer.appendChild(legend);
}

function addRadioButtons() {
    const radioButtons = document.createElement('div');
    radioButtons.id = 'radioButtons-heatmap';
    radioButtons.innerHTML = `
    <label><input type="radio" name="heatmap" value="bikes" checked> Bikes HeatMap</label>
    <label><input type="radio" name="heatmap" value="stands"> Stands HeatMap</label>
    <label><input type="radio" name="heatmap" value="none"> None</label>
    `;

    const mapContainer = document.getElementById('map');
    mapContainer.appendChild(radioButtons);

    radioButtons.addEventListener('change', (event) => {
        if (event.target.value === 'bikes') {
            window.heatmapBikes.setMap(window.googleMap);
            window.heatmapStands.setMap(null);
            document.getElementById('heatmapLegend').style.display = 'block';
            document.getElementById('heatmapLegend-title').innerHTML = 'Available Bikes';
        } else if (event.target.value === 'stands') {
            window.heatmapBikes.setMap(null);
            window.heatmapStands.setMap(window.googleMap);
            document.getElementById('heatmapLegend').style.display = 'block';
            document.getElementById('heatmapLegend-title').innerHTML = 'Available Stands';
        } else if (event.target.value === 'none') {
            window.heatmapBikes.setMap(null);
            window.heatmapStands.setMap(null);
            document.getElementById('heatmapLegend').style.display = 'none';
        }
    });
}

export { addStationMarker }