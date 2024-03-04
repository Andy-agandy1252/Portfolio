document.addEventListener("DOMContentLoaded", function() {
    // Ensure coordinates value is valid
    var coordinates = document.getElementById('coordinates').value;

    if (coordinates) {
        // Split the coordinates string into latitude and longitude
        var [latitude, longitude] = coordinates.split(',').map(parseFloat);

        if (!isNaN(latitude) && !isNaN(longitude)) {
            // Initialize the map
            var map = L.map('map').setView([latitude, longitude], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

            // Add a marker for the reported location
            var reportMarker = L.marker([latitude, longitude]).addTo(map);

            var streetMarker;
            var coordinatesMarker;
            var loadingDiv = document.getElementById('loading');

            function showLoading() {
                if (loadingDiv) {
                    loadingDiv.style.display = 'block';
                } else {
                    loadingDiv = document.createElement('div');
                    loadingDiv.id = 'loading';
                    loadingDiv.textContent = 'Loading...';
                    document.body.appendChild(loadingDiv);
                }
            }

            function hideLoading() {
                if (loadingDiv) {
                    loadingDiv.style.display = 'none';
                }
            }

            function addStreetMarker(lat, lon) {
                if (streetMarker) {
                    map.removeLayer(streetMarker);
                }

                document.getElementById('street').value = 'Loading';
                showLoading();

                fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&addressdetails=1&extratags=1`)
                    .then(response => response.json())
                    .then(data => {
                        var street = data.address.road || '';
                        var houseNumber = data.address.house_number || '';
                        var city = data.address.city || '';
                        var postalCode = data.address.postcode || '';
                        var state = data.address.state || '';
                        var country = data.address.country || '';

                        document.getElementById('street').value = street;
                        document.getElementById('house_number').value = houseNumber;
                        document.getElementById('city').value = city;
                        document.getElementById('zipcode').value = postalCode;
                        document.getElementById('region').value = state;
                        document.getElementById('country').value = country;

                        hideLoading();
                        streetMarker = L.marker([lat, lon]).addTo(map);
                    });
            }

            function addCoordinatesMarker(lat, lon) {
                if (coordinatesMarker) {
                    map.removeLayer(coordinatesMarker);
                }

                document.getElementById('coordinates').value = `${lat}, ${lon}`;
                coordinatesMarker = L.marker([lat, lon]).addTo(map);
            }

            map.on('click', function (e) {
                var lat = e.latlng.lat;
                var lon = e.latlng.lng;

                document.getElementById('street').value = 'Loading';
                addStreetMarker(lat, lon);

                document.getElementById('coordinates').value = `${lat}, ${lon}`;
                addCoordinatesMarker(lat, lon);
            });
        } else {
            console.error('Invalid latitude or longitude values');
        }
    } else {
        console.error('No coordinates provided');
    }

    function clearLocationInputs() {
        document.getElementById('street').value = '';
        document.getElementById('house_number').value = '';
        document.getElementById('city').value = '';
        document.getElementById('zipcode').value = '';
        document.getElementById('region').value = '';
        document.getElementById('country').value = '';

        if (streetMarker) {
            map.removeLayer(streetMarker);
        }
        if (coordinatesMarker) {
            map.removeLayer(coordinatesMarker);
        }

        document.getElementById('coordinates').value = '';
    }

    function placeLocationManually() {
        var street = document.getElementById('street').value;
        var houseNumber = document.getElementById('house_number').value;
        var city = document.getElementById('city').value;
        var region = document.getElementById('region').value;
        var country = document.getElementById('country').value;

        if (!street || !city || !region || !country) {
            alert('Please fill in the required fields: Street, City, Region, Country');
            return;
        }

        var fullAddress = street + ' ' + houseNumber + ', ' + city + ', ' + region + ', ' + country;

        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(fullAddress)}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    var lat = data[0].lat;
                    var lon = data[0].lon;

                    document.getElementById('coordinates').value = `${lat}, ${lon}`;

                    if (coordinatesMarker) {
                        map.removeLayer(coordinatesMarker);
                    }

                    coordinatesMarker = L.marker([lat, lon]).addTo(map);
                } else {
                    alert('Location not found. Please check the address.');
                    clearLocationInputs();
                }
            });
    }
});
