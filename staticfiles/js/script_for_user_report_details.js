// script_for_user_report_details.js

function initializeMap(coordinates) {
    if (coordinates) {
        // Split the coordinates string into latitude and longitude
        var [latitude, longitude] = coordinates.split(',').map(parseFloat);

        if (!isNaN(latitude) && !isNaN(longitude)) {
            // Initialize the map
            var map = L.map('map').setView([latitude, longitude], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

            // Add a marker for the reported location
            var reportMarker = L.marker([latitude, longitude]).addTo(map);
        } else {
            console.error('Invalid latitude or longitude values');
        }
    } else {
        console.error('No coordinates provided');
    }
}

// Trigger the map initialization when the DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // Extract coordinates from the element's data attribute
    var coordinatesElement = document.getElementById('map');
    var coordinates = coordinatesElement.dataset.coordinates;

    // Call the initializeMap function with the extracted coordinates
    initializeMap(coordinates);
});
