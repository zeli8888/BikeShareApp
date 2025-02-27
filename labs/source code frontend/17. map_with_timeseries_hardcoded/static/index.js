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

            google.charts.setOnLoadCallback(drawChart);

            // Defining the function drawChart
            function drawChart(){
                const chartData = new google.visualization.DataTable();
                chartData.addColumn('datetime', 'Time'); // First column as datetime
                chartData.addColumn('number', 'Available Bikes'); // Numeric columns
                chartData.addColumn('number', 'Free Stands');

                // Add rows with datetime objects for the time column
                chartData.addRows([
                    [new Date(2024, 11, 4, 8, 0), 12, 8], // Dec 4, 2024, 08:00 AM
                    [new Date(2024, 11, 4, 9, 0), 15, 5], // Dec 4, 2024, 09:00 AM
                    [new Date(2024, 11, 4, 10, 0), 10, 10], // Dec 4, 2024, 10:00 AM
                    [new Date(2024, 11, 4, 11, 0), 8, 12], // Dec 4, 2024, 11:00 AM
                    [new Date(2024, 11, 4, 12, 0), 14, 6], // Dec 4, 2024, 12:00 PM
                ]);

                // Chart options
                const options = {
                    title: 'Station Time Series Overview',
                    legend: { position: 'bottom' },
                    curveType: 'function', // Smooth the lines
                    hAxis: {
                        title: 'Time of Day',
                        format: 'HH:mm', // Display hours and minutes
                    },
                    vAxis: {
                        title: 'Count',
                    },
                    width: 400,
                    height: 250,
                };

                // Draw the chart
                const chart = new google.visualization.LineChart(
                    document.getElementById(`chart_div_${station.number}`)
                );

                chart.draw(chartData, options);

            }
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
