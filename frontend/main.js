// Import Leaflet library
import L from 'leaflet';

// Create map instance
const map = L.map('map').setView([0, 0], 2); // Default view with center at [0, 0] and zoom level 2

// Add tile layer (e.g., OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Example satellite position
const satLatLng = L.latLng(31.767600, -106.43502); // Replace with actual latitude and longitude

// Add marker for satellite
const satMarker = L.marker(satLatLng).addTo(map);
satMarker.bindPopup('Satellite Position'); // Add a popup

// Zoom to satellite position
map.setView(satLatLng, 4); // Zoom level 4

// TODO: Fetch and update satellite positions dynamically
// You'll need to update the satellite positions using AJAX/fetch requests and update the marker position.
