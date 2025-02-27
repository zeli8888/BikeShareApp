function addMarkers(stations) {
    console.log(stations); // use this to see what is the content of stations
    for (const station of stations) {
        var marker = new google.maps.Marker({
            position: {
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
        });
    }
}

function getStations() {
    // Send a request to the "/stations" endpoint to retrieve station data.
    fetch("/stations")
        .then((response) => {
            // Convert the response to JSON format (assuming the response is JSON).
            return response.json();
        })
        .then((data) => {
            // Log the type of the fetched data and verify it in the console.
            console.log("fetch response", typeof data);

            // Call the `addMarkers` function to place markers on the map
            // using the data received from the server.
            addMarkers(data);
        })
        .catch((error) => {
            // Log an error if the fetch request fails.
            console.error("Error fetching stations data:", error);
        });
}


// Initialize and add the map
function initMap() {
    const dublin = { lat: 53.35014, lng: -6.266155 };

    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });

    getStations();
}

var map = null;
window.initMap = initMap;
