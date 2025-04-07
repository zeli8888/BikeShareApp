/**
 * Fetches weather data from backend and updates the current weather, daily forecast and hourly forecast elements.
 * @param {string} weatherUrl - The URL of the backend weather data.
 * @param {number} [latitude] - The latitude for which to retrieve the weather data.
 * @param {number} [longitude] - The longitude for which to retrieve the weather data.
 * @returns {Promise} A promise that resolves when all elements are updated or rejects with an error if there is a problem.
 */
async function getWeather(weatherUrl, latitude = null, longitude = null) {
    // Add latitude and longitude parameters if provided
    if (latitude != null && longitude != null) {
        weatherUrl += `?latitude=${latitude}&longitude=${longitude}`;
    }
    try {
        const response = await fetch(weatherUrl);
        const data = await response.json();

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
                        <button id="current-weather-button" title="update" onclick="getCurrentWeather(${latitude}, ${longitude}, '${current.district}')">
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
        data.hourly.slice(1, 25).forEach(hour => {
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

        return Promise.resolve(); // Return a resolved promise after all updates are complete

    } catch (error) {
        console.error('Error loading weather data:', error);
        document.getElementById('weather-info-container').innerHTML = "Error fetching weather data.";
        return Promise.reject(error); // Reject the promise to handle error situation
    }
}

/**
 * Updates the current weather data for a given district using the
 * current weather API endpoint. This function adds a rotating
 * icon to the button while the request is pending, and removes it
 * after the request is complete. If the request is successful, it
 * shows a success alert. If the request fails, it shows an error
 * alert.
 * 
 * New data is guaranteed to be fetched from external api calls.
 * 
 * @param {number} latitude - The latitude of the district.
 * @param {number} longitude - The longitude of the district.
 * @param {string} district - The name of the district.
 */
async function getCurrentWeather(latitude, longitude, district) {
    const button = document.getElementById('current-weather-button');
    button.classList.add('rotate-icon');
    try {
        await getWeather(window.CURRENT_WEATHER_URL, latitude, longitude);
        window.alert(`Current Weather Data for ${district} has been updated.`);
    } catch (error) {
        const button = document.getElementById('current-weather-button');
        button.classList.remove('rotate-icon');
        console.error('Error updating weather data:', error);
        window.alert('Failed to update weather data. Please try again later.');
    }
}

export { getWeather, getCurrentWeather };