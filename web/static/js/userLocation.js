import { showWeatherInfoContainer } from "./sidebar.js";
/**
 * Retrieves the user's current location and updates the map's center to the user's location.
 * The user's location is stored in the userLocationMarker and the user's location is stored in session storage.
 * If the user's location could not be retrieved, an error is shown to the user.
 * @return {Promise} A promise that resolves when the user's location has been retrieved and the map has been updated.
 * @throws {Error} If the browser does not support geolocation.
 */
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
                showWeatherInfoContainer();
                showPosition(position);
                window.userLocationMarker.position = new google.maps.LatLng(window.coords.latitude, window.coords.longitude);
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

/**
 * Shows a alert box with the user's location information, and resets the button back to "Share Location".
 * @param {Object} position - The user's location information from the Geolocation API.
 */
function showPosition(position) {
    alert("Location Information Received: \nLatitude: " + position.coords.latitude +
        "\nLongitude: " + position.coords.longitude);
    const button = document.getElementById("share-location-button");
    button.innerHTML = "Share Location"
}

/**
 * Shows an alert box with a message describing the error that occurred when trying to
 * retrieve the user's location, and resets the button back to "Share Location".
 * @param {Object} error - The error object from the Geolocation API.
 */
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