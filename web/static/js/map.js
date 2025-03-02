async function initMap() {
    // The location of Dublin
    const location = {
        lat: 53.3498,
        lng: -6.2603
    };
    let map = new google.maps.Map(document.getElementById("map"), {
        mapId: GOOGLE_MAP_ID,
        center: location,
        zoom: 13,
    });

    window.map = map;
}

// Load the Google Maps API asynchronously
document.addEventListener('DOMContentLoaded', function () {
    const googleMapScript = document.createElement('script');
    googleMapScript.src = "https://maps.googleapis.com/maps/api/js?key=" + GOOGLE_MAP_KEY + "&callback=initMap&libraries=marker&loading=async";
    googleMapScript.async = true;
    document.body.appendChild(googleMapScript);
});