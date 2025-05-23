/**
 * Fetches prediction data for a given station.
 *
 * Args:
 *     stationId (number): The ID of the station.
 *     latitude (number): The latitude of the station.
 *     longitude (number): The longitude of the station.
 *
 * Returns:
 *     Promise<Array>: A promise that resolves to an array of prediction data for the station. If an error occurs or data is invalid, it returns an empty array.
 */
async function fetchPredictionData(stationId, latitude, longitude) {
    try {
        const response = await fetch(window.PREDICTION_URL.slice(0, -1) + stationId + `?latitude=${latitude}&longitude=${longitude}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!Array.isArray(data)) {
            throw new Error("Invalid response format");
        }
        return data;
    } catch (error) {
        console.error(`Error fetching prediction data for station ${stationId}:`, error);
        return [];
    }
}

/**
 * Renders a prediction chart for the selected station.
 * 
 * If the selected station has already been rendered, no action is taken.
 * Otherwise, fetches prediction data for the station and displays it using Google Charts. If no data is available, displays a message indicating the lack of prediction data.
 * 
 * Handles errors by logging them to the console.
 */
async function renderBikePredictionChart() {
    try {
        if (window.chosenStation && window.chosenStation === window.lastPredictedStation) return;
        const container = document.getElementById('station-prediction');
        container.innerHTML = 'Predicting, please wait...';
        window.lastPredictedStation = window.chosenStation;
        const data = await fetchPredictionData(window.chosenStation, window.chosenStationPosition.lat, window.chosenStationPosition.lng);
        if (!data.length) {
            container.innerHTML = `Sorry, no prediction data available <br>for station ${window.chosenStationName}`;
            return
        };
        google.charts.load('current', { packages: ['corechart'] });
        google.charts.setOnLoadCallback(() => drawChart(data));
    } catch (error) {
        console.error("Error rendering bike trend chart:", error);
    }
}

/**
 * Draws a Google Charts line chart in the 'station-prediction' div,
 * representing the predicted bike and stand availability for the chosen station.
 * 
 * Args:
 *     data (Array): An array of objects containing the properties 'future_dt',
 *     'available_bikes', and 'available_stands'.
 * 
 * The function ensures that the number of available bikes and stands
 * does not exceed the maximum number of stands for the station.
 * The chart is drawn with responsive text size within the container.
 */

function drawChart(data) {
    const chartData = new google.visualization.DataTable();

    // Define columns
    chartData.addColumn('datetime', 'Time'); // x-axis (Date/Time)
    chartData.addColumn('number', 'Bikes'); // y-axis (Bikes)
    chartData.addColumn('number', 'Stands'); // y-axis (Stands)

    // Populate chart rows with fetched data
    data.forEach((entry) => {
        const availableBikes = Math.min(Math.max(entry.available_bikes, 0), window.chosenStationBikeStands);
        const availableStands = Math.min(Math.max(entry.available_stands, 0), window.chosenStationBikeStands);
        chartData.addRow([
            new Date(entry.future_dt),
            availableBikes,      // Bikes count
            availableStands,      // Bikes stands count
        ]);
    });

    const container = document.getElementById('station-prediction');
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
        title: `24 Hour Prediction for \n${window.chosenStationName}`,
        titleTextStyle: {
            fontSize: fontSize + 3,
            bold: true,
        },
        hAxis: {
            title: 'Time',
            format: 'HH:mm',
            titleTextStyle: { fontSize: fontSize }, // Set font size for x-axis title
            textStyle: { fontSize: fontSize }, // Set font size for x-axis labels
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

export { renderBikePredictionChart };
