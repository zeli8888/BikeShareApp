function addMarkers(stations) {
    console.log(stations); // Use this to see the content of stations

    for (const station of stations) {
        // Create a marker for each station
        const marker = new google.maps.Marker({
            position: {
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
            icon: 'https://icons.iconarchive.com/icons/aha-soft/transport/48/bike-icon.png',
        });

        // Create an empty infowindow
        const infoWindow = new google.maps.InfoWindow({});

        // Add a click listener to the marker to show the info window
        marker.addListener("click", () => {
            // Define container for the chart
            const chartContainer = document.createElement('div');
            chartContainer.style.width = '300px';
            chartContainer.style.height = '200px';

            // Info window content (including chart div placeholder with this id)
            const content = `
                <div>
                    <h3>${station.name}</h3>
                    <p><strong>Address:</strong> ${station.address || "N/A"}</p>
                    <p><strong>Available Bike Stands:</strong> ${station.bikestands || "N/A"}</p>
                    <div id="chart_div_${station.number}" style="width: 300px; height: 200px;"></div>
                </div>
            `;

            // Set the content
            infoWindow.setContent(content);

            // Open the window
            infoWindow.open(map, marker);

            // Fetch the station-specific data and draw the chart
            fetch(`/available/${station.number}`)
                .then((response) => response.json())
                .then((data) => {
                    // Load Google Charts library
                    google.charts.load('current', { packages: ['corechart'] });

                    // When the library is ready, draw the chart (calling the function drawChart)
                    google.charts.setOnLoadCallback(() => drawChart(data, station.number));
                })
                .catch((error) => {
                    console.error(`Error fetching data for station ${station.number}:`, error);
                });
        });
    }
}

// Function to draw the chart using Google Charts
function drawChart(data, stationId) {
    const chartData = new google.visualization.DataTable();

    // Define columns
    chartData.addColumn('datetime', 'Time'); // x-axis (Date/Time)
    chartData.addColumn('number', 'Available Bikes'); // y-axis (Bikes)

    // Populate chart rows with fetched data
    data.forEach((entry) => {
        chartData.addRow([
            new Date(entry.last_update), // Convert timestamp to Date
            entry.available_bikes,      // Bikes count
        ]);
    });

    // Chart options
    const options = {
        title: `Available Bikes at Station ${stationId}`,
        hAxis: {
            title: 'Time',
            format: 'HH:mm', // Format time as hours and minutes
        },
        vAxis: {
            title: 'Available Bikes',
        },
        curveType: 'function', // Smooth line
        legend: { position: 'bottom' },
        width: 400,
        height: 250,
    };

    // Draw the chart in the placeholder div
    const chart = new google.visualization.LineChart(
        document.getElementById(`chart_div_${stationId}`)
    );

    chart.draw(chartData, options);
}


function getStations() {
    // Send a request to the "/stations" endpoint to retrieve station data
    fetch("/stations")
        .then((response) => {
            // Convert the response to JSON format
            return response.json();
        })
        .then((data) => {
            // Log the type of the fetched data and verify it in the console
            console.log("fetch response", typeof data);

            // Call the `addMarkers` function to place markers on the map
            // using the data received from the server
            addMarkers(data);
        })
        .catch((error) => {
            // Log an error if the fetch request fails
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
