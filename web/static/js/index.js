import { loadGoogleMapsApi, initMap } from "./map.js";
import { getLocation } from "./user_location.js";
import { calculateAndDisplayRoute, getStationRoute } from "./route.js"
import { show_weather_info_container, toggle_sidebar_content } from "./sidebar.js";
import { getCurrentBikes } from "./stations.js";
import { getCurrentWeather } from "./weather.js";

const button = document.getElementById("share-location-button");
button.addEventListener("click", getLocation);

window.show_weather_info_container = show_weather_info_container;
window.toggle_sidebar_content = toggle_sidebar_content;
window.calculateAndDisplayRoute = calculateAndDisplayRoute;
window.getStationRoute = getStationRoute;
window.getCurrentBikes = getCurrentBikes;
window.getCurrentWeather = getCurrentWeather;

document.getElementById("travel-mode").addEventListener("change", () => {
    calculateAndDisplayRoute(window.target_lat, window.target_lng, document.getElementById("travel-mode").value, window.start_lat, window.start_lng);
});

const storedLocation = sessionStorage.getItem('userLocation');
if (storedLocation && storedLocation !== 'undefined') {
    window.coords = JSON.parse(storedLocation);
} else {
    window.coords = {
        latitude: 53.3498,
        longitude: -6.2603
    }
}
show_weather_info_container();

// Function to fetch hourly data for a district and display it
function getHourlyData(district) {
    fetch(`/api/hourly/${district}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                // Handle error (maybe show a message to the user)
            } else {
                console.log('Hourly Data:', data);
                // Now you can use this data to update the page (e.g., show it in a table)
                displayHourlyData(data);
            }
        })
        .catch(error => {
            console.error('Error fetching hourly data:', error);
        });
}

// Function to display the hourly data on the page
function displayHourlyData(data) {
    const hourlyForecastContainer = document.getElementById('hourly-forecast');
    hourlyForecastContainer.innerHTML = ''; // Clear previous data

    // Iterate through the data and create an HTML representation
    data.forEach(hourly => {
        const hourlyElement = document.createElement('div');
        hourlyElement.innerHTML = `
            <p>Time: ${hourly.future_dt}</p>
            <p>Temperature: ${hourly.temp}°C</p>
            <p>Weather: ${hourly.weather_description}</p>
            <hr>
        `;
        hourlyForecastContainer.appendChild(hourlyElement);
    });
}

getHourlyData();


// Trigger hourly data fetch when the user inputs a district name
document.getElementById('des-input').addEventListener('change', function() {
    const district = this.value.trim(); // Get the district from the input field
    if (district) {
        getHourlyData(district); // Fetch hourly data for the district
    } else {
        console.log("Please enter a valid district.");
    }
});


window.initMap = initMap;
loadGoogleMapsApi();