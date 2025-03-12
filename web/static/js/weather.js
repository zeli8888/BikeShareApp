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
            document.getElementById('weather-icon').src = `https://openweathermap.org/img/wn/${weatherIconCode}@2x.png`;
            document.getElementById('weather-desc').innerHTML = `
                ${district}
                <br>
                ${weatherDescription}
                <br>Temperature: ${temperatureC}°C
                <br>Feels Like: ${feels_like}°C
                <br>
                <br>Last Update: <br>${lastUpdated}
                `;
        }).catch(error => {
            console.error('Error loading weather data:', error);
            document.getElementById('weather-desc').innerHTML = "Error fetching weather data.";
        });
}

export { getWeather }