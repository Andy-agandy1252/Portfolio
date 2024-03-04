function initMapAndGeocoding(city, country) {
    var geocoder = L.Control.Geocoder.nominatim();

    // Geocode the city and country
    geocoder.geocode(city + ', ' + country, function (results) {
        if (results && results.length > 0) {
            var location = results[0].center;
            var latitude = location.lat;
            var longitude = location.lng;

            // Log the coordinates
            console.log("Geocoded Coordinates:", latitude, longitude);

            // Set up the map view
            var map = L.map('map').setView([latitude, longitude], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

            var streetMarker;
            var coordinatesMarker;
            var loadingDiv = document.getElementById('loading');

            function showLoading() {
                if (loadingDiv) {
                    loadingDiv.style.display = 'block';
                } else {
                    console.error('Loading div not found.');
                }
            }

            function hideLoading() {
                loadingDiv.style.display = 'none';
            }

            function addStreetMarker(lat, lon) {
                if (streetMarker) {
                    console.log('Street Coordinates:', lat, lon);
                    map.removeLayer(streetMarker);
                }
                // Set input value to "Loading"
                document.getElementById('street').value = 'Loading';
                // Show loading screen while fetching address
                showLoading();
                // Reverse geocoding using Nominatim
                fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&addressdetails=1&extratags=1`)
                    .then(response => response.json())
                    .then(data => {
                        // Store the entire data object
                        var fullAddressData = data;
                        // Extract relevant information (if needed)
                        var street = data.address.road || '';
                        var houseNumber = data.address.house_number || '';
                        var city = data.address.city || '';
                        var postalCode = data.address.postcode || '';
                        var state = data.address.state || '';
                        var country = data.address.country || '';

                        // Set the values for the respective input fields
                        document.getElementById('street').value = street;
                        document.getElementById('house_number').value = houseNumber;
                        document.getElementById('city').value = city;
                        document.getElementById('zipcode').value = postalCode;
                        document.getElementById('region').value = state;
                        document.getElementById('country').value = country;

                        // Hide loading screen after fetching address
                        hideLoading();

                        // Add the street marker after fetching the address
                        streetMarker = L.marker([lat, lon]).addTo(map);
                    });
            }

function addCoordinatesMarker(lat, lon) {
    if (coordinatesMarker) {
        console.log('Coordinates:', lat, lon);
        map.removeLayer(coordinatesMarker);
    }
    // Set input value to coordinates
    document.getElementById('coordinates').value = `${lat}, ${lon}`;
    // Add the coordinates marker
    coordinatesMarker = L.marker([lat, lon]).addTo(map);

    // Reposition the map view to center on the marker
    map.panTo([lat, lon]);
}



            map.on('click', function (e) {
                var lat = e.latlng.lat;
                var lon = e.latlng.lng;
                document.getElementById('street').value = 'Loading';
                addStreetMarker(lat, lon);
                document.getElementById('coordinates').value = `${lat}, ${lon}`;
                addCoordinatesMarker(lat, lon);
            });

            // Define the function globally so it can be accessed from HTML
window.placeLocationManually = function() {
    // Retrieve values from input fields
    var street = document.getElementById('street').value;
    var houseNumber = document.getElementById('house_number').value;
    var city = document.getElementById('city').value;
    var region = document.getElementById('region').value;
    var country = document.getElementById('country').value;

    // Check if any of the required fields are empty
    if (!street || !city || !region || !country) {
        alert('Please fill in the required fields: Street, City, Region, Country');
        return;
    }

    // Construct the full address
    var fullAddress = street + ' ' + houseNumber + ', ' + city + ', ' + region + ', ' + country;

    // Use Nominatim to get coordinates based on the manually entered address
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(fullAddress)}`)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                var lat = data[0].lat;
                var lon = data[0].lon;

                // Update the coordinates input field
                document.getElementById('coordinates').value = `${lat}, ${lon}`;

                // Remove existing coordinates marker
                if (coordinatesMarker) {
                    map.removeLayer(coordinatesMarker);
                }

                // Add a new coordinates marker
                coordinatesMarker = L.marker([lat, lon]).addTo(map);

                // Reposition the map view to center on the marker
                map.panTo([lat, lon]);
            } else {
                // Alert user about invalid address and clear input fields on OK
                alert('Location not found. Please check the address.');
                clearLocationInputs();
            }
        });
};


// Define the function globally so it can be accessed from HTML
window.clearLocationInputs = function() {
    // Clear values in input fields
    document.getElementById('street').value = '';
    document.getElementById('house_number').value = '';
    document.getElementById('city').value = '';
    document.getElementById('zipcode').value = '';
    document.getElementById('region').value = '';
    document.getElementById('country').value = '';

    // Remove existing markers from the map
    if (streetMarker) {
        map.removeLayer(streetMarker);
    }
    if (coordinatesMarker) {
        map.removeLayer(coordinatesMarker);
    }

    // Clear the coordinates input field
    document.getElementById('coordinates').value = '';
};


            // Rest of your script...

            // Initialize the issue type from URL parameters
            document.addEventListener("DOMContentLoaded", function () {
                const urlParams = new URLSearchParams(window.location.search);
                const issueType = urlParams.get('issue_type');
                if (issueType) {
                    document.getElementById('issue_type').value = issueType;
                }
            });
        } else {
            console.error("Geocoding failed. No results.");
        }
    });
}
// At the bottom of your script_for_create_report.js file
window.placeLocationManually = function() {
    // Your function implementation here
};