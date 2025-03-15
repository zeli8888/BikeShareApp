function getWeather(weatherUrl) {
    fetch(weatherUrl)
        .then(response => response.json())
        .then(data => {
            const currentWeather = data.current;
            const weatherDescription = currentWeather.weather_description;
            const weatherIconCode = currentWeather.weather_icon;
            const temperatureC = (currentWeather.temp - 273.15).toFixed(1); // Convert Kelvin to Celsius
            const feels_like = (currentWeather.feels_like - 273.15).toFixed(1); // Convert Kelvin to Celsius
            const lastUpdated = currentWeather.dt;
            const district = currentWeather.district;
            // Update weather icon and description
            document.getElementById('weather-desc').innerHTML = `
                ${district}
                <br>
                ${weatherDescription}<img id="weather-icon" src="" alt="Weather Icon" />
                <br>Temperature: ${temperatureC}°C
                <br>Feels Like: ${feels_like}°C
                <br><br>
                <p id="last-updated">Last Update: ${lastUpdated}</p>
                `;
            document.getElementById('weather-icon').src = `https://openweathermap.org/img/wn/${weatherIconCode}@2x.png`;
        }).catch(error => {
            console.error('Error loading weather data:', error);
            document.getElementById('weather-desc').innerHTML = "Error fetching weather data.";
        });
}

export { getWeather }