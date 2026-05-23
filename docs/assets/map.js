// ALCHEMYTIMELINEMAP Interactive Map
// Leaflet.js-based visualization with location details, events, and mouseover tooltips

let map;
let locationMarkers = {};
let eventsByLocation = {};
let allData = {};

// Region color scheme (distinct colors for different areas)
const regionColors = {
  "Egypt": "#D4A574",          // Sandy brown
  "Iraq": "#A0522D",            // Saddle brown
  "Persia": "#CD853F",          // Peru
  "Syria": "#DAA520",           // Goldenrod
  "Spain": "#FF6347",           // Tomato
  "Sicily": "#FF8C00",          // Dark orange
  "Germany": "#4169E1",         // Royal blue
  "England": "#6495ED",         // Cornflower blue
  "Italy": "#DC143C",           // Crimson
  "France/Alsace": "#8B008B",   // Dark magenta
  "France": "#8B008B",          // Dark magenta
  "Austria": "#9370DB",         // Medium purple
  "Bohemia": "#4B0082",         // Indigo
  "Switzerland": "#32CD32",     // Lime green
  "Denmark/Sweden": "#87CEEB"   // Sky blue
};

// Initialize map centered on Mediterranean
function initMap() {
  map = L.map('map').setView([35, 15], 4);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
    minZoom: 2
  }).addTo(map);

  // Load data and create markers
  loadAndDisplayData();

  // Add legend
  addLegend();

  // Add era filter controls
  addEraFilter();
}

// Load data from data.json and create markers/popups
function loadAndDisplayData() {
  fetch('data/data.json')
    .then(response => response.json())
    .then(data => {
      allData = data;

      // Build index of events by location
      data.events.forEach(event => {
        const loc = event.location_slug;
        if (!eventsByLocation[loc]) {
          eventsByLocation[loc] = [];
        }
        eventsByLocation[loc].push(event);
      });

      // Load enhanced location data
      fetch('data/locations_enhanced.json')
        .then(resp => resp.json())
        .then(locData => {
          locData.locations.forEach(location => {
            createLocationMarker(location, data);
          });
        });
    });
}

// Create marker for each location with detailed popup
function createLocationMarker(location, data) {
  const color = regionColors[location.region] || "#808080";

  // Get events at this location
  const eventsAtLocation = eventsByLocation[location.slug] || [];
  const eventsWithDescriptions = eventsAtLocation.filter(e => e.description && e.description !== "STUB");

  // Create HTML for marker popup
  let popupHTML = `
    <div class="location-popup" style="max-width: 400px;">
      <h3 style="margin: 0 0 10px 0; color: ${color}; font-size: 16px; border-bottom: 2px solid ${color}; padding-bottom: 8px;">
        ${location.place_name}
      </h3>
      <p style="margin: 8px 0; font-size: 12px; color: #666;">
        <strong>Modern name:</strong> ${location.modern_name}<br>
        <strong>Region:</strong> ${location.region}
      </p>
      <div style="margin: 10px 0; padding: 8px; background-color: #f9f9f9; border-left: 3px solid ${color}; font-size: 13px;">
        <strong>Alchemical Significance:</strong><br>
        ${location.alchemical_significance}
      </div>
      <div style="margin: 10px 0; font-size: 13px;">
        <strong>Events at this location:</strong> ${eventsAtLocation.length}<br>
        ${eventsWithDescriptions.length > 0 ?
          `<strong>Documented events:</strong> ${eventsWithDescriptions.length}` :
          '<em>No detailed descriptions yet</em>'}
      </div>
  `;

  // Add key figures if available
  if (location.key_figures && location.key_figures.length > 0) {
    popupHTML += `
      <div style="margin: 10px 0; font-size: 13px;">
        <strong>Key figures:</strong>
        <ul style="margin: 5px 0; padding-left: 20px;">
    `;
    location.key_figures.forEach(slug => {
      const person = data.persons.find(p => p.slug === slug);
      if (person) {
        popupHTML += `<li><a href="../persons/${slug}.html">${person.name}</a></li>`;
      }
    });
    popupHTML += `</ul></div>`;
  }

  // Add timeline of events
  if (eventsAtLocation.length > 0) {
    popupHTML += `
      <div style="margin: 10px 0; font-size: 12px;">
        <strong>Timeline of events:</strong>
        <ul style="margin: 5px 0; padding-left: 20px; max-height: 200px; overflow-y: auto;">
    `;

    // Sort events by date
    eventsAtLocation.sort((a, b) => a.date_start_year - b.date_start_year);

    eventsAtLocation.forEach(event => {
      popupHTML += `<li>${event.date_label}</li>`;
    });
    popupHTML += `</ul></div>`;
  }

  popupHTML += `</div>`;

  // Create custom icon
  const icon = L.divIcon({
    html: `<div style="background-color: ${color}; border: 2px solid white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">●</div>`,
    className: 'location-marker',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });

  // Create marker with tooltip
  const marker = L.marker([location.latitude, location.longitude], { icon: icon });

  // Mouseover tooltip
  const tooltipContent = `
    <strong>${location.place_name}</strong><br>
    ${eventsAtLocation.length} event${eventsAtLocation.length !== 1 ? 's' : ''}
  `;

  marker.bindTooltip(tooltipContent, {
    permanent: false,
    direction: 'top',
    offset: [0, -10],
    className: 'location-tooltip'
  });

  // Click popup
  marker.bindPopup(popupHTML, {
    maxWidth: 420,
    minWidth: 300,
    className: 'location-popup-container'
  });

  marker.addTo(map);
  locationMarkers[location.slug] = marker;
}

// Add legend showing regions and event counts
function addLegend() {
  const legend = L.control({ position: 'bottomright' });

  legend.onAdd = function(map) {
    const div = L.DomUtil.create('div', 'legend');
    div.innerHTML = `
      <div style="background: white; padding: 12px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2); max-height: 300px; overflow-y: auto;">
        <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #333;">Regions</h4>
        <div style="font-size: 12px;">
          ${Object.entries(regionColors).map(([region, color]) => `
            <div style="margin: 5px 0; display: flex; align-items: center;">
              <span style="display: inline-block; width: 16px; height: 16px; background-color: ${color}; border-radius: 50%; margin-right: 8px; border: 1px solid #ddd;"></span>
              ${region}
            </div>
          `).join('')}
        </div>
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        <h4 style="margin: 10px 0 5px 0; font-size: 12px; color: #666;">
          <strong>Total Events:</strong> ${Object.values(eventsByLocation).reduce((sum, arr) => sum + arr.length, 0)}
        </h4>
      </div>
    `;
    return div;
  };

  legend.addTo(map);
}

// Add era filter controls
function addEraFilter() {
  const eraControl = L.control({ position: 'topleft' });

  eraControl.onAdd = function(map) {
    const div = L.DomUtil.create('div', 'era-control');
    div.innerHTML = `
      <div style="background: white; padding: 10px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 8px 0; font-size: 13px;">Filter by Era</h4>
        <div style="font-size: 12px;">
          <label style="display: block; margin: 5px 0;">
            <input type="radio" name="era" value="all" checked> All Events
          </label>
          <label style="display: block; margin: 5px 0;">
            <input type="radio" name="era" value="LATE_ANTIQUE"> Late Antique (300-600)
          </label>
          <label style="display: block; margin: 5px 0;">
            <input type="radio" name="era" value="MEDIEVAL"> Medieval (600-1450)
          </label>
          <label style="display: block; margin: 5px 0;">
            <input type="radio" name="era" value="RENAISSANCE"> Renaissance (1450-1550)
          </label>
          <label style="display: block; margin: 5px 0;">
            <input type="radio" name="era" value="EARLY_MODERN"> Early Modern (1550-1700)
          </label>
        </div>
      </div>
    `;

    // Add event listeners for era filters
    div.querySelectorAll('input[name="era"]').forEach(input => {
      input.addEventListener('change', (e) => {
        filterByEra(e.target.value);
      });
    });

    return div;
  };

  eraControl.addTo(map);
}

// Filter locations by era
function filterByEra(era) {
  Object.entries(locationMarkers).forEach(([slug, marker]) => {
    if (era === 'all') {
      marker.setOpacity(1);
    } else {
      // Check if location has events in this era
      const eventsInEra = eventsByLocation[slug] && eventsByLocation[slug].some(e => {
        // Map date ranges to eras
        const year = e.date_start_year;
        if (era === 'LATE_ANTIQUE') return year >= 300 && year < 600;
        if (era === 'MEDIEVAL') return year >= 600 && year < 1450;
        if (era === 'RENAISSANCE') return year >= 1450 && year < 1550;
        if (era === 'EARLY_MODERN') return year >= 1550 && year < 1700;
        return false;
      });

      marker.setOpacity(eventsInEra ? 1 : 0.3);
    }
  });
}

// Style customizations
const style = document.createElement('style');
style.textContent = `
  .location-tooltip {
    background-color: #333 !important;
    color: white !important;
    border-radius: 4px !important;
    padding: 6px 10px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
  }

  .location-popup-container .leaflet-popup-content {
    margin: 0 !important;
    padding: 0 !important;
  }

  .location-popup {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #333;
  }

  .location-popup a {
    color: #0066cc;
    text-decoration: none;
  }

  .location-popup a:hover {
    text-decoration: underline;
  }

  .era-control {
    z-index: 400;
  }
`;
document.head.appendChild(style);

// Initialize map when page loads
document.addEventListener('DOMContentLoaded', initMap);
