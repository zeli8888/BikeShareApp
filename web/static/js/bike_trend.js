async function fetchBikeTrendData() {
    try {
        const response = await fetch(window.BIKES_ONE_DAY_URL);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!Array.isArray(data)) {
            throw new Error("Invalid response format");
        }
        return data;
    } catch (error) {
        console.error("Error fetching bike trend data:", error);
        return [];
    }
}

async function renderBikeTrendChart() {
    try {
        const data = await fetchBikeTrendData();
        if (!data.length) return;
        
        const labels = data.map(entry => entry.last_update ? new Date(entry.last_update).toLocaleTimeString() : "N/A");
        const values = data.map(entry => entry.available_bikes || 0);

        const chartElement = document.getElementById("bikeTrendChart");
        if (!chartElement) {
            console.error("Chart element not found");
            return;
        }

        const ctx = chartElement.getContext("2d");
        if (!ctx) {
            console.error("Failed to get 2D context");
            return;
        }

        new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Available Bikes",
                    data: values,
                    borderColor: "blue",
                    fill: false,
                }]
            }
        });
    } catch (error) {
        console.error("Error rendering bike trend chart:", error);
    }
}

function initBikeTrendFeature() {
    document.addEventListener("DOMContentLoaded", function () {
        const toggleTrendButton = document.getElementById("toggle-trend");
        if (!toggleTrendButton) {
            console.error("Toggle trend button not found");
            return;
        }
        toggleTrendButton.addEventListener("click", function () {
            const trendContainer = document.getElementById("trend-container");
            if (!trendContainer) {
                console.error("Trend container not found");
                return;
            }
            if (trendContainer.style.display === "none") {
                trendContainer.style.display = "block";
                try {
                    renderBikeTrendChart();
                } catch (error) {
                    console.error("Error rendering bike trend chart:", error);
                }
            } else {
                trendContainer.style.display = "none";
            }
        });
    });
}

// Export function for `index.js`
export { initBikeTrendFeature };
