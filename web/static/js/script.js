// Wait until the page fully loads
document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map centered on Dublin
    var map = L.map('map').setView([53.3498, -6.2603], 13);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Initialize marker clustering
    var markers = L.markerClusterGroup();

    // Function to determine marker color based on available bikes
    function getMarkerColor(bikes) {
        if (bikes >= 10) return "green"; // High availability
        if (bikes >= 5) return "yellow"; // Medium availability
        return "red"; // Low availability
    }

    // Add a legend
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function(map) {
        const div = L.DomUtil.create("div", "info legend");
        div.innerHTML += "<h4>Bike Availability</h4>";
        div.innerHTML += '<i style="background: green"></i> 10+ Bikes<br>';
        div.innerHTML += '<i style="background: yellow"></i> 5-9 Bikes<br>';
        div.innerHTML += '<i style="background: red"></i> 0-4 Bikes<br>';
        return div;
    };

    legend.addTo(map);

    // Fetch the stations data
    fetch('stations.json')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Loaded stations:", data.length); // Debugging

            // Add markers for each station
            data.forEach(station => {
                if (!station.position || !station.position.lat || !station.position.lng) {
                    console.error("Invalid station data:", station);
                    return;
                }

                // Determine the marker color based on available bikes
                const color = getMarkerColor(station.available_bikes);

                // Create a custom marker using Leaflet circle marker
                let marker = L.circleMarker([station.position.lat, station.position.lng], {
                        radius: 8,
                        color: color,
                        fillColor: color,
                        fillOpacity: 0.7
                    })
                    .bindPopup(` 
                    <b>${station.name}</b><br>
                    🚲 Bikes Available: ${station.available_bikes}<br>
                    🅿️ Parking Spaces: ${station.bike_stands - station.available_bike_stands || "N/A"}
                `);

                // Add the marker to the cluster group
                markers.addLayer(marker);
            });

            // Add the clustered markers to the map
            map.addLayer(markers);
        })
        .catch(error => console.error('Error loading station data:', error));

    // Fetch the weather data
    fetch('weather.json')
        .then(response => response.json())
        .then(data => {
            console.log("Loaded weather data:", data); // Debugging

            const currentWeather = data.current;
            const weatherDescription = currentWeather.weather[0].description;
            const weatherIconCode = currentWeather.weather[0].icon;
            const temperatureK = currentWeather.temp; // Temperature in Kelvin
            const temperatureC = (temperatureK - 273.15).toFixed(1); // Convert to Celsius

            // Forecast for next 2 days
            const dailyForecast = data.daily.slice(1, 3); // Get data for the next 2 days
            let forecastHtml = '';

            dailyForecast.forEach((day, index) => {
                const dayTempK = day.temp.day; // Daytime temperature
                const dayTempC = (dayTempK - 273.15).toFixed(1); // Convert to Celsius
                const dayWeatherDescription = day.weather[0].description;
                const dayWeatherIcon = day.weather[0].icon;

                forecastHtml += `
                    <div style="margin-top: 10px;">
                        <p><strong>Day ${index + 1}:</strong> ${dayWeatherDescription}</p>
                        <img src="http://openweathermap.org/img/wn/${dayWeatherIcon}@2x.png" alt="${dayWeatherDescription}">
                        <p>Temp: ${dayTempC}°C</p>
                    </div>
                `;
            });

            // Create weather container
            const weatherContainer = document.createElement('div');
            weatherContainer.classList.add('weather-container');

            // Create current weather icon
            const weatherIcon = document.createElement('img');
            weatherIcon.src = `http://openweathermap.org/img/wn/${weatherIconCode}@2x.png`;
            weatherIcon.alt = weatherDescription;

            // Create temperature and description text for current weather
            const weatherInfo = document.createElement('p');
            weatherInfo.innerHTML = `Current Weather:<br>${weatherDescription}<br>Temperature: ${temperatureC}°C`;

            // Append current weather info to the container
            weatherContainer.appendChild(weatherIcon);
            weatherContainer.appendChild(weatherInfo);

            // Append forecast information
            weatherContainer.innerHTML += forecastHtml;


            // Add weather info to the body
            document.body.appendChild(weatherContainer);
        })
        .catch(error => console.error('Error loading weather data:', error));
});