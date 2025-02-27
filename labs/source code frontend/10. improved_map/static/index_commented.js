// Declare a global variable `map` to store the map instance.
// Declaring it globally allows it to be accessed outside the `initMap` function if needed.
var map; 

// Define the `initMap` function which will initialize the Google Map
function initMap() {
    // Create an object representing Dublin's latitude and longitude coordinates.
    const dublin = { lat: 53.350140, lng: -6.266155 };
    
    // Create a new map instance centered at Dublin.
    // The `google.maps.Map` constructor is used to bind the map to the HTML element with the ID "map".
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12, // Zoom level of the map
        center: dublin, // Center the map at Dublin's coordinates
    });

    // Add a marker to the map, positioned at Dublin's coordinates.
    const marker = new google.maps.Marker({
        position: dublin, // Position the marker at Dublin
        map: map,         // Add the marker to the map instance
    });
}

// Expose the `initMap` function as a global function.
// This step is necessary because Google Maps API needs to call `initMap`
// when the `callback` parameter is specified in the script URL.
// Without this, Google Maps would not know where to find the function.
window.initMap = initMap;

