// Global scope
var map; // Declare the map variable in the global scope

document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('map');
    var isAuthenticated = mapContainer !== null; // Replace with actual condition

    // Initialize the map
    map = L.map(mapContainer).setView([52.5200, 13.4050], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    if (isAuthenticated) {
        // Code for authenticated users
        var city = mapContainer.getAttribute('data-city');
        var country = mapContainer.getAttribute('data-country');

        // Perform geocoding to get coordinates for the city
        getCityCoordinates(city, country);
    } else {
        // Code for non-authenticated users
        // Add markers for each user report
        addMarkersForUserReports();
    }
});

// Define getCityCoordinates in the global scope
function getCityCoordinates(city, country) {
    var geocoder = L.Control.Geocoder.nominatim();

    // Geocode the city and country
    geocoder.geocode(city + ', ' + country, function (results) {
        if (results && results.length > 0) {
            var location = results[0].center;
            var latitude = location.lat;
            var longitude = location.lng;

            // Log the coordinates
            console.log("Geocoded Coordinates:", latitude, longitude);

            // Update the map view
            map.setView([latitude, longitude], 13);

            // Add markers for each user report
            addMarkersForUserReports();
        } else {
            console.error("Geocoding failed. No results.");
        }
    });
}

// Define addMarkersForUserReports in the global scope
function addMarkersForUserReports() {
    var reportElements = document.querySelectorAll('.user-report');
    reportElements.forEach(function(element) {
        var reportCoordinates = element.getAttribute('data-coordinates').split(',').map(parseFloat);
        var reportStreet = element.getAttribute('data-street');
        var reportHouseNumber = element.getAttribute('data-house-number');
        var reportCity = element.getAttribute('data-city');
        var reportZipcode = element.getAttribute('data-zipcode');
        var reportCountry = element.getAttribute('data-country');
        var reportIssueType = element.getAttribute('data-issue-type');
        var reportUrl = element.getAttribute('data-url');

        if (!isNaN(reportCoordinates[0]) && !isNaN(reportCoordinates[1])) {
            var reportMarker = L.marker(reportCoordinates).addTo(map);
            reportMarker.bindPopup(
                `<strong>Location:</strong> ${reportStreet} ${reportHouseNumber}, ${reportCity}, ${reportZipcode}, ${reportCountry}<br>
                <strong>Issue Type:</strong> ${reportIssueType}<br>
                <a href="${reportUrl}">View Details</a>`
            ); // Customize the popup content
        }
    });
}
