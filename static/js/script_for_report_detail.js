document.addEventListener('DOMContentLoaded', function() {
    var mapElement = document.getElementById('map');
    var coordinates = mapElement.getAttribute('data-coordinates').split(',').map(parseFloat);

    if (coordinates[0] !== 0 || coordinates[1] !== 0) {
        var map = L.map('map').setView(coordinates, 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // Get additional data from data attributes
        var street = mapElement.getAttribute('data-street');
        var houseNumber = mapElement.getAttribute('data-house-number');
        var city = mapElement.getAttribute('data-city');
        var zipcode = mapElement.getAttribute('data-zipcode');
        var country = mapElement.getAttribute('data-country');
        var issueType = mapElement.getAttribute('data-issue-type');

        // Add a marker for the reported location
        var marker = L.marker(coordinates).addTo(map);
        marker.bindPopup(
            `<strong>Location:</strong> ${street} ${houseNumber}, ${city}, ${zipcode}, ${country}<br>
            <strong>Issue Type:</strong>${issueType}<br>
            <a href="${window.location.href}">View Details</a>`
        ); // Customize the popup content
    }
});
