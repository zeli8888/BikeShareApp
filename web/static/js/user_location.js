import { show_weather_info_container } from "./sidebar.js";
function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            const button = document.getElementById("share-location-button");
            button.innerHTML = "Fetching Location, Please Wait..."
            const options = {
                enableHighAccuracy: false,
                timeout: 5000,
                maximumAge: Infinity,
            };
            navigator.geolocation.getCurrentPosition(position => {
                window.coords = position.coords;
                sessionStorage.setItem('userLocation', JSON.stringify(window.coords));
                show_weather_info_container();
                showPosition(position);
                window.user_location_marker.position = new google.maps.LatLng(window.coords.latitude, window.coords.longitude);
                window.googleMap.setCenter({ lat: window.coords.latitude, lng: window.coords.longitude });
                resolve();
            }, error => {
                showError(error);
                resolve();
            }, options);
        } else {
            reject(new Error('Geolocation is not supported by this browser.'));
        }
    });
}

function showPosition(position) {
    alert("Location Information Received: \nLatitude: " + position.coords.latitude +
        "\nLongitude: " + position.coords.longitude);
    const button = document.getElementById("share-location-button");
    button.innerHTML = "Share Location"
}

function showError(error) {
    const button = document.getElementById("share-location-button");
    button.innerHTML = "Share Location"
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert(
                "Geolocation Request Denied\r\r" +
                "Don't worry, it's an easy fix! If your browser is treating this site as unsecure, you can add an exception for this url to allow geolocation access.\r\r" +
                "Here's how:\r" +
                "  • For Edge: Go to edge://flags/#unsafely-treat-insecure-origin-as-secure\r" +
                "  • For Chrome: Go to chrome://flags/#unsafely-treat-insecure-origin-as-secure"
            );
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.\r\rPlease try again.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

export { getLocation }