function getWeather(weatherUrl, latitude = null, longitude = null) {
    if (latitude !== null && longitude !== null) {
        weatherUrl += `?latitude=${latitude}&longitude=${longitude}`;
    }
    fetch(weatherUrl)
        .then(response => response.json())
        .then(data => {
            // Clear previous data
            document.getElementById('current-details').innerHTML = '';
            document.getElementById('daily-forecast').innerHTML = '';
            document.getElementById('hourly-forecast').innerHTML = '';

            // Display current weather
            const current = data.current;
            const currentDetails = `
                <div class="current-details-grid">
                    <div>
                        <h3>
                            ${current.district}                            
                            <button id="current-weather-button" title="update">
                                &#x21bb;
                            </button>
                        </h3>
                        <img class="weather-icon" src="https://openweathermap.org/img/wn/${current.weather_icon}@2x.png">
                        <div>${current.weather_main}</div>
                        <div class="temp-info">
                            ${(current.temp - 273.15).toFixed(1)}°C
                        </div>
                        <div>Feels like ${(current.feels_like - 273.15).toFixed(1)}°C</div>
                    </div>
                    <div>
                        <div>Humidity: ${current.humidity}%</div>
                        <div>Pressure: ${current.pressure} hPa</div>
                        <div>Wind: ${current.wind_speed} m/s</div>
                        <div>Visibility: ${current.visibility / 1000} km</div>
                        <div>Sunrise: ${new Date(current.sunrise).toLocaleTimeString()}</div>
                        <div>Sunset: ${new Date(current.sunset).toLocaleTimeString()}</div>
                        <div>LastUpdate: ${new Date(current.dt).toLocaleTimeString()}</div>
                    </div>
                </div>
            `;
            document.getElementById('current-details').innerHTML = currentDetails;

            // Add event listener for update button
            document
                .getElementById('current-weather-button')
                .addEventListener('click', () => getWeather(window.CURRENT_WEATHER_URL, latitude, longitude));

            // Display daily forecast
            data.daily.forEach(day => {
                const dayElement = document.createElement('div');
                dayElement.className = 'forecast-item';
                dayElement.innerHTML = `
                    <div>${new Date(day.future_dt).toLocaleDateString('en-US', { weekday: 'short' })}</div>
                    <img class="weather-icon" src="https://openweathermap.org/img/wn/${day.weather_icon}@2x.png">
                    <div>${(day.temp_max - 273.15).toFixed(1)}°C</div>
                    <div>${(day.temp_min - 273.15).toFixed(1)}°C</div>
                    <div class="forecast-description">${day.weather_main}</div>
                `;
                document.getElementById('daily-forecast').appendChild(dayElement);
            });

            // Display hourly forecast
            data.hourly.slice(0, 24).forEach(hour => {
                const hourElement = document.createElement('div');
                hourElement.className = 'forecast-item';
                hourElement.innerHTML = `
                    <div>${new Date(hour.future_dt).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</div>
                    <img class="weather-icon" src="https://openweathermap.org/img/wn/${hour.weather_icon}@2x.png">
                    <div>${(hour.temp - 273.15).toFixed(1)}°C</div>
                    <div  class="forecast-description">${hour.weather_main}</div>
                `;
                document.getElementById('hourly-forecast').appendChild(hourElement);
            });

        }).catch(error => {
            console.error('Error loading weather data:', error);
            document.getElementById('weather-info-container').innerHTML = "Error fetching weather data.";
        });
}

export { getWeather };