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
    fetch("/stations")
        .then((response) => {
            return response.json();
        })
        .then((data) => {

            console.log("fetch response", typeof data);
            addMarkers(data);
        })
        .catch((error) => {
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
