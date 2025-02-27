function addMarkers(stations) {
    console.log(stations); // Use this to see the content of stations

    for (const station of stations) {
        // Create a marker for each station: MAKE SURE IT IS CONST, so it is not overwritten
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

        // Create an empty infowindow: MAKE SURE IT IS CONST, so it is not overwritten
        const infoWindow = new google.maps.InfoWindow({});

        // Add a click listener to the marker to show the info window
        marker.addListener("click", () => {

            // Define container for the chart
            const chartContainer = document.createElement('div');
            chartContainer.style.width = '300px';
            chartContainer.style.height = '200px';

            // Info window content (including chart div placeholder with this id: 
            // chart_div_${station.number}). The $ is used to include
            // data about js variables in the HTML. 
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

            // Now start drawing the chart
            google.charts.load('current', { packages: ['corechart'] });

            google.charts.setOnLoadCallback(() => {
                // Hardcoded data for the chart
                const chartData = new google.visualization.DataTable();
                chartData.addColumn('string', 'Type');
                chartData.addColumn('number', 'Count');
                chartData.addRows([
                    ['Available Bikes', station.bikestands],  // Value for bike stands
                    ['Free Stands', station.available_bikes], // Value for available bike stands: 
                                                              // if this is in a separate table, Flask will 
                                                              // need to join the two tables, and then pass 
                                                              // this joined table in the stations page
                ]);

                // Chart options
                const options = {
                    title: 'Station Overview',
                    legend: { position: 'bottom' },
                    width: 300,
                    height: 200,
                };

                // Draw the chart
                const chart = new google.visualization.BarChart(
                    document.getElementById(`chart_div_${station.number}`)
                );

                chart.draw(chartData, options);
            });
        });
    }
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
