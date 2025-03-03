async function fetchStation() {
    try {
        const [stations, availabilities] = await Promise.all([
            fetch('api/stations').then(response => response.json()),
            fetch('api/availabilities/latest').then(response => response.json())
        ]);

        return { stations, availabilities };
    } catch (error) {
        console.error(error);
    }
}

async function addStationMarker() {
    map = window.map;
    const { stations, availabilities } = await fetchStation();
    window.markers = {};

    stations.forEach(station => {
        const { address, banking, bike_stands, name, number, position_lat, position_lng } = station;

        // Create AdvancedMarkerElement
        const marker = new google.maps.marker.AdvancedMarkerElement({
            position: new google.maps.LatLng(position_lat, position_lng),
            map: map,
            title: name,  // Tooltip for marker
            ariaLabel: name // Accessible name for screen readers
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `
                        <div style="font-family: Arial, sans-serif; font-size: 14px; color: #000;">
                            <strong>${name}</strong><br>
                            Address: ${address}<br>
                        </div>
                              `
        });

        marker.addListener("gmp-click", () => {
            infoWindow.open(map, marker);
        });

        marker.infoWindow = infoWindow;
        window.markers[number] = marker;
    });

    availabilities.forEach(availability => {
        const { available_bike_stands, available_bikes, last_update, number, status } = availability;
        const infoWindow = window.markers[number].infoWindow;
        infoWindow.setContent(infoWindow.content + `
            <div style="font-family: Arial, sans-serif; font-size: 14px; color: #000;">
                Available Bikes: ${available_bikes}<br>
                Available Stands: ${available_bike_stands}<br>
                Status: ${status}<br>
                Last Update: ${last_update}
            </div>
          `);
    });
}

addStationMarker()