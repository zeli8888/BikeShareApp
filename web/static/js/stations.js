import { showStationInfoContainer } from "./sidebar.js";
import { getWeather } from "./weather.js";

async function addStationMarker(bikesUrl) {
    try {
        const { stations, availabilities } = await fetch(bikesUrl).then(response => response.json());
        window.markers = {};

        // Create AdvancedMarkerElement For User Location
        const userLocationMarkerImg = document.createElement('img');
        userLocationMarkerImg.src = "https://maps.google.com/mapfiles/ms/micons/yellow-dot.png";
        window.userLocationMarker = new google.maps.marker.AdvancedMarkerElement({
            position: new google.maps.LatLng(window.coords.latitude, window.coords.longitude),
            map: window.googleMap,
            content: userLocationMarkerImg,
            title: 'YOUR LOCATION'
        });

        const stationMarkerImg = document.createElement('img');
        stationMarkerImg.src = "https://maps.google.com/mapfiles/ms/micons/red-dot.png";
        stations.forEach(station => {
            setStation(station, stationMarkerImg);
        });

        const { heatmapBikesData, heatmapStandsData } = setAvailabilities(availabilities);
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
    } catch (error) {
        console.error('Error adding station markers:', error);
        alert('Error adding station markers. Please try again later.');
    }
}

function addLegend() {
    const legend = document.createElement('div');
    legend.id = 'heatmap-legend';
    legend.innerHTML = `
    <div id="heatmap-legend-title" class="legend-title">Available Bikes</div>
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
    radioButtons.id = 'radio-buttons-heatmap';
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
            document.getElementById('heatmap-legend').style.display = 'block';
            document.getElementById('heatmap-legend-title').innerHTML = 'Available Bikes';
        } else if (event.target.value === 'stands') {
            window.heatmapBikes.setMap(null);
            window.heatmapStands.setMap(window.googleMap);
            document.getElementById('heatmap-legend').style.display = 'block';
            document.getElementById('heatmap-legend-title').innerHTML = 'Available Stands';
        } else if (event.target.value === 'none') {
            window.heatmapBikes.setMap(null);
            window.heatmapStands.setMap(null);
            document.getElementById('heatmap-legend').style.display = 'none';
        }
    });
}

async function getCurrentBikes() {
    const buttons = document.getElementsByClassName('current-bikes-button');
    for (const button of buttons) {
        button.classList.add('rotate-icon');
    }
    try {
        const { stations, availabilities } = await fetch(window.CURRENT_BIKES_URL).then(response => response.json());
        const stationMarkerImg = document.createElement('img');
        stationMarkerImg.src = "https://maps.google.com/mapfiles/ms/micons/red-dot.png";

        stations.forEach(station => {
            const { address, banking, bike_stands, name, number, position_lat, position_lng } = station;
            if (number in window.markers) {
                window.markers[number].infoWindow.setContent(`
                <div class="info-window-content">
                    <span class="info-window-title"><strong>${name}</strong></span>
                    <button class="current-bikes-button" title="update" onclick="getCurrentBikes()">
                        &#x21bb;
                    </button>
                    <br>
                    <a href="#" onclick="getStationRoute(${position_lat}, ${position_lng})">➡️Directions<br></a>
                    <!-- Banking: ${banking}<br> -->
                    <!-- Bike Stands: ${bike_stands}<br> -->
                </div>
            `
                );
            } else {
                setStation(station, stationMarkerImg);
            }
        });

        const { heatmapBikesData, heatmapStandsData } = setAvailabilities(availabilities, true);
        window.heatmapBikes.setData(heatmapBikesData);
        window.heatmapStands.setData(heatmapStandsData);
        window.alert('Current Bikes Data has been updated.');
    } catch (error) {
        console.error('Error updating current bikes data:', error);
        window.alert('Error updating current bikes data. Please try again later.');
    } finally {
        for (let i = 0; i < buttons.length; i++) {
            const button = buttons[i];
            if (button) {
                button.classList.remove('rotate-icon');
            }
        }
        // infoWindow will be re-rendered with new content, so no need to remove old buttons.
        // This is to stop rotating buttons that have no current data to update.
    }
}

function setStation(station, stationMarkerImg) {
    const { address, banking, bike_stands, name, number, position_lat, position_lng } = station;
    const markerImg = stationMarkerImg.cloneNode(true);
    // Create AdvancedMarkerElement
    const marker = new google.maps.marker.AdvancedMarkerElement({
        position: new google.maps.LatLng(position_lat, position_lng),
        map: window.googleMap,
        content: markerImg,
        title: name,  // Tooltip for marker
        ariaLabel: name // Accessible name for screen readers
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="info-window-content">
                <span class="info-window-title"><strong>${name}</strong></span>
                <button class="current-bikes-button" title="update" onclick="getCurrentBikes()">
                    &#x21bb;
                </button>
                <br>
                <a href="#" onclick="getStationRoute(${position_lat}, ${position_lng})">➡️Directions<br></a>
                <!-- Banking: ${banking}<br> -->
                <!-- Bike Stands: ${bike_stands}<br> -->
            </div>
            `
    });

    marker.addListener("gmp-click", () => {
        infoWindow.open(window.googleMap, marker);
        document.getElementById('station-info').innerHTML = infoWindow.content;
        getWeather(window.WEATHER_URL, position_lat, position_lng);
        window.chosenStation = number; // for the use of daily trend, prediction and current information in side bar
        window.chosenStationName = address; // for the use of daily trend and prediction in side bar
        window.chosenStationPosition = { lat: position_lat, lng: position_lng }; // for the use of prediction in side bar
        window.chosenStationBikeStands = bike_stands; // for the use of prediction in side bar
        showStationInfoContainer();
    });

    marker.infoWindow = infoWindow;
    window.markers[number] = marker;
}

function setAvailabilities(availabilities, updateSidebar = false) {
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
        if (updateSidebar && window.chosenStation === number) {
            document.getElementById('station-info').innerHTML = infoWindow.content;
        }
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
    return {
        heatmapBikesData: heatmapBikesData,
        heatmapStandsData: heatmapStandsData
    };
}

export { addStationMarker, getCurrentBikes }