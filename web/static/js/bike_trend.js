async function fetchBikeTrendData(station_id) {
    try {
        const response = await fetch(window.BIKES_ONE_DAY_STATION_URL.replace("{}", station_id));
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!Array.isArray(data)) {
            throw new Error("Invalid response format");
        }
        return data;
    } catch (error) {
        console.error(`Error fetching data for station ${station_id}:`, error);
        return [];
    }
}

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
