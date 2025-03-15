async function addStationMarker(bikesUrl) {
    const map = window.googleMap;
    const { stations, availabilities } = await fetch(bikesUrl).then(response => response.json());
    window.markers = {};

    // Create AdvancedMarkerElement For User Location
    const user_location_marker_img = document.createElement('img');
    user_location_marker_img.src = "https://maps.google.com/mapfiles/ms/micons/yellow-dot.png";
    window.user_location_marker = new google.maps.marker.AdvancedMarkerElement({
        position: window.coords ? new google.maps.LatLng(window.coords.latitude, window.coords.longitude) : new google.maps.LatLng(53.3498, -6.2603),
        map: map,
        content: user_location_marker_img,
        title: 'YOUR LOCATION'
    });

    const station_marker_img = document.createElement('img');
    station_marker_img.src = "https://maps.google.com/mapfiles/ms/micons/red-dot.png";
    stations.forEach(station => {
        const { address, banking, bike_stands, name, number, position_lat, position_lng } = station;
        const marker_img = station_marker_img.cloneNode(true);
        // Create AdvancedMarkerElement
        const marker = new google.maps.marker.AdvancedMarkerElement({
            position: new google.maps.LatLng(position_lat, position_lng),
            map: map,
            content: marker_img,
            title: name,  // Tooltip for marker
            ariaLabel: name // Accessible name for screen readers
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `
              <div class="info-window-content">
                <strong>${name}</strong>
                <a href="https://www.google.com/maps/dir/?api=1&destination=${position_lat},${position_lng}" target="_blank">➡️Directions</a>
                <a href="#" onclick="calculateAndDisplayRoute(${position_lat}, ${position_lng}, 'DRIVING')">➡️Directions<br></a>
                Banking: ${banking}<br>
                Bike Stands: ${bike_stands}<br>
              </div>
            `
        });

        marker.addListener("gmp-click", () => {
            window.chosen_station = station;
            infoWindow.open(map, marker);
        });

        marker.infoWindow = infoWindow;
        window.markers[number] = marker;
    });

    availabilities.forEach(availability => {
        const { available_bike_stands, available_bikes, last_update, number, status } = availability;
        const infoWindow = window.markers[number].infoWindow;
        infoWindow.setContent(infoWindow.content + `
            <div class="info-window-content">
                Available Bikes: ${available_bikes}<br>
                Available Stands: ${available_bike_stands}<br>
                Status: ${status}<br>
                Last Update: ${last_update}
            </div>
          `);
    });
}

export { addStationMarker }