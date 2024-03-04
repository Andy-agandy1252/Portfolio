var map; // Declare the map variable in the global scope

document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('map');
    var isAuthenticated = mapContainer.hasAttribute('data-city') && mapContainer.hasAttribute('data-country');

    console.log('Is Authenticated:', isAuthenticated); // Debugging statement

    // Initialize the map with default coordinates for Berlin
    map = L.map(mapContainer).setView([52.52, 13.405], 13); // Removed 'var' to assign to the global 'map' variable

    // Add a tile layer for the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Add markers, polygons, etc. to the map as needed

    if (isAuthenticated) {
        // Code for authenticated users
        var city = mapContainer.getAttribute('data-city');
        var country = mapContainer.getAttribute('data-country');

        console.log('City:', city, 'Country:', country);
        // Perform geocoding to get coordinates for the city
        getCityCoordinates(city, country);
    } else {
        // Code for non-authenticated users
        // Add markers for each report
        addMarkersForReports(reportsData);

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

            // Call the function to add markers after updating the map view
            addMarkersForReports(reportsData);
        } else {
            console.error("Geocoding failed. No results.");
        }
    });
}

// Define addMarkersForReports in the global scope
function addMarkersForReports(reports) {
    // Iterate over the reports array and add markers to the map
    reports.forEach(function(report) {
        var coordinates = report.coordinates.split(',').map(parseFloat);
        if (!isNaN(coordinates[0]) && !isNaN(coordinates[1])) {
            var marker = L.marker(coordinates).addTo(map);
            marker.bindPopup(
                `<strong>Location:</strong> ${report.street} ${report.house_number}, ${report.city}, ${report.zipcode}, ${report.country}<br>
                <strong>Issue Type:</strong> ${report.issue_type}<br>
                <a href="${report.url}">View Details</a>` // This should work if report.url is set correctly
            ); // Customize the popup content
        }
    });
}

// Define searchCity in the global scope
function searchCity() {
    var cityInput = document.getElementById('searchCityInput').value;
    var countryInput = document.getElementById('searchCountryInput').value;

    if (cityInput) {
        getCityCoordinates(cityInput, countryInput);
    } else {
        alert('Please enter a city name.');
    }
}