import { getWeather } from "./weather.js";
function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                window.coords = position.coords;
                sessionStorage.setItem('userLocation', JSON.stringify(window.coords));
                getWeather(window.WEATHER_URL + `?latitude=${window.coords.latitude}&longitude=${window.coords.longitude}`);
                showPosition(position);
                window.user_location_marker.position = new google.maps.LatLng(window.coords.latitude, window.coords.longitude);
                window.googleMap.setCenter({ lat: window.coords.latitude, lng: window.coords.longitude });
                resolve();
            }, error => {
                showError(error);
                resolve();
            });
        } else {
            reject(new Error('Geolocation is not supported by this browser.'));
        }
    });
}

function showPosition(position) {
    alert("Location Information Received: \nLatitude: " + position.coords.latitude +
        "\nLongitude: " + position.coords.longitude);
}

function showError(error) {

    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("You have denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

export { getLocation }