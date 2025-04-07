/**
 * Fetches one day's bike availability data for a specific station.
 *
 * Args:
 *     stationId (number): The ID of the station for which to retrieve data.
 *
 * Returns:
 *     Promise<Array>: A promise that resolves to an array of availability data for the station. 
 *     If an error occurs or data is invalid, it returns an empty array.
 */
async function fetchBikeTrendData(stationId) {
    try {
        const response = await fetch(window.BIKES_ONE_DAY_STATION_URL.replace("{}", stationId));
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!Array.isArray(data)) {
            throw new Error("Invalid response format");
        }
        return data;
    } catch (error) {
        console.error(`Error fetching data for station ${stationId}:`, error);
        return [];
    }
}

/**
 * Renders a bike trend chart for the selected station.
 * 
 * If the selected station has already been rendered, no action is taken.
 * Otherwise, fetches one day's availability data for the station and 
 * displays it using Google Charts. If no data is available, displays 
 * a message indicating the lack of history data.
 * 
 * Handles errors by logging them to the console.
 */

async function renderBikeTrendChart() {
    try {
        if (window.chosenStation && window.chosenStation === window.lastShownStation) return;
        const container = document.getElementById('station-daily-trend');
        container.innerHTML = 'Fetching history data, please wait...';
        window.lastShownStation = window.chosenStation;
        const data = await fetchBikeTrendData(window.chosenStation);
        if (!data.length) {
            container.innerHTML = `Sorry, no history data available <br>for station ${window.chosenStationName}`;
            return
        };
        google.charts.load('current', { packages: ['corechart'] });
        google.charts.setOnLoadCallback(() => drawChart(data));
    } catch (error) {
        console.error("Error rendering bike trend chart:", error);
    }
}

/**
 * Draws a Google Charts line chart in the 'station-daily-trend' div,
 * representing the daily bike availability trend for the chosen station.
 * 
 * Args:
 *     data (Array): An array of objects containing the properties 'last_update', 'available_bikes', and 'available_bike_stands'.
 */
function drawChart(data) {
    const chartData = new google.visualization.DataTable();

    // Define columns
    chartData.addColumn('datetime', 'Time'); // x-axis (Date/Time)
    chartData.addColumn('number', 'Bikes'); // y-axis (Bikes)
    chartData.addColumn('number', 'Stands'); // y-axis (Stands)

    // Populate chart rows with fetched data
    data.forEach((entry) => {
        chartData.addRow([
            new Date(entry.last_update), // Convert timestamp to Date
            entry.available_bikes,      // Bikes count
            entry.available_bike_stands,      // Bikes stands count
        ]);
    });

    const container = document.getElementById('station-daily-trend');
    container.innerHTML = ''; // Clear any existing chart
    // Create the chart with responsive text size
    const options = resizeChartText(container);

    // Draw the chart in the placeholder div
    const chart = new google.visualization.LineChart(
        container
    );

    chart.draw(chartData, options);
}

/**
 * Returns an options object for a Google Charts line chart that scales the
 * text size based on the width of the given container.
 *
 * Args:
 *     container (Element): The container element to render the chart in.
 *
 * Returns:
 *     Object: An options object for a Google Charts line chart.
 */
function resizeChartText(container) {
    const containerWidth = container.offsetWidth;
    var fontSize = containerWidth / 28; // Adjust the ratio as needed
    fontSize = Math.max(fontSize, 10);

    return {
        title: `History Daily Trend for \n${window.chosenStationName}`,
        titleTextStyle: {
            fontSize: fontSize + 3,
            bold: true,
        },
        hAxis: {
            title: 'Time',
            format: 'HH:mm',
            titleTextStyle: { fontSize: fontSize }, // Set font size for x-axis title
            textStyle: { fontSize: fontSize } // Set font size for x-axis labels
        },
        vAxis: {
            title: 'Count',
            viewWindow: {
                min: 0
            },
            titleTextStyle: { fontSize: fontSize }, // Set font size for y-axis title
            textStyle: { fontSize: fontSize } // Set font size for y-axis labels
        },
        series: [
            { label: 'Bikes', color: '#008000' },
            { label: 'Stands', color: '#0000FF' },
        ],
        curveType: 'function',
        legend: { position: 'bottom', textStyle: { fontSize: fontSize } }, // Set font size for legend
        backgroundColor: '#f5f5f5',
        width: '100%',
        height: '100%',
    };
}

export { renderBikeTrendChart };
