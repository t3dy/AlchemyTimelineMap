// ALCHEMYTIMELINEMAP interactive map
// Data-driven Leaflet map with alias resolution, fallback locations, and filters.

let map;
let allData = null;
let locationMarkers = {};
let locationIndex = new Map();
let eventsByLocation = new Map();

const regionColors = {
  Egypt: "#D4A574",
  Iraq: "#A0522D",
  Persia: "#CD853F",
  Syria: "#DAA520",
  Spain: "#FF6347",
  Sicily: "#FF8C00",
  Germany: "#4169E1",
  England: "#6495ED",
  Italy: "#DC143C",
  "France/Alsace": "#8B008B",
  France: "#8B008B",
  Austria: "#9370DB",
  Bohemia: "#4B0082",
  Switzerland: "#32CD32",
  "Denmark/Sweden": "#87CEEB",
  "Low Countries": "#2E8B57",
  Greece: "#20B2AA",
  Byzantium: "#9932CC",
  Iberia: "#FF7F50"
};

const locationAliases = {
  rayy: "ray",
  venice: "ven-island",
  venetia: "ven-island",
  basel: "basle"
};

const fallbackLocations = [
  {
    slug: "amsterdam",
    place_name: "Amsterdam",
    latitude: 52.3676,
    longitude: 4.9041,
    region: "Low Countries",
    modern_name: "Amsterdam, Netherlands",
    alchemical_significance:
      "Major early modern printing and commercial center where alchemical books, instruments, and laboratory supplies circulated through the Republic's trade networks.",
    key_periods: ["EARLY_MODERN"]
  },
  {
    slug: "antwerp",
    place_name: "Antwerp",
    latitude: 51.2194,
    longitude: 4.4025,
    region: "Low Countries",
    modern_name: "Antwerp, Belgium",
    alchemical_significance:
      "A major Low Countries commercial center that helped circulate alchemical books, pigments, metals, and laboratory equipment between the Mediterranean and northern Europe.",
    key_periods: ["RENAISSANCE", "EARLY_MODERN"]
  },
  {
    slug: "athens",
    place_name: "Athens",
    latitude: 37.9838,
    longitude: 23.7275,
    region: "Greece",
    modern_name: "Athens, Greece",
    alchemical_significance:
      "A classical and late antique intellectual center whose philosophical traditions remained important for the transmission of Greek natural philosophy into later alchemical writing.",
    key_periods: ["ANTIQUITY", "LATE_ANTIQUE"]
  },
  {
    slug: "bruges",
    place_name: "Bruges",
    latitude: 51.2093,
    longitude: 3.2247,
    region: "Low Countries",
    modern_name: "Bruges, Belgium",
    alchemical_significance:
      "A key urban workshop and trade center in the Low Countries where artisanal practice, exchange, and manuscript circulation supported alchemical experimentation.",
    key_periods: ["RENAISSANCE", "EARLY_MODERN"]
  },
  {
    slug: "cambridge",
    place_name: "Cambridge",
    latitude: 52.2053,
    longitude: 0.1218,
    region: "England",
    modern_name: "Cambridge, England",
    alchemical_significance:
      "An academic center associated with early modern natural philosophy and the circulation of chymical ideas in England.",
    key_periods: ["EARLY_MODERN"]
  },
  {
    slug: "canterbury",
    place_name: "Canterbury",
    latitude: 51.2802,
    longitude: 1.0789,
    region: "England",
    modern_name: "Canterbury, England",
    alchemical_significance:
      "An ecclesiastical center that helped sustain learned exchange, manuscript culture, and medicinal or laboratory knowledge in medieval England.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "cluny",
    place_name: "Cluny",
    latitude: 46.4336,
    longitude: 4.6602,
    region: "France",
    modern_name: "Cluny, France",
    alchemical_significance:
      "A monastic center that supported manuscript culture, translation, and the transmission of practical and natural-philosophical knowledge in medieval Europe.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "constantinople",
    place_name: "Constantinople",
    latitude: 41.0082,
    longitude: 28.9784,
    region: "Byzantium",
    modern_name: "Istanbul, Turkey",
    alchemical_significance:
      "The imperial capital of Byzantium and a major conduit for the preservation and adaptation of Greek technical learning, including alchemical and pharmaceutical traditions.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "fulda",
    place_name: "Fulda",
    latitude: 50.5558,
    longitude: 9.6836,
    region: "Germany",
    modern_name: "Fulda, Germany",
    alchemical_significance:
      "A monastic and scholarly center in central Europe whose libraries and scriptoria preserved natural-philosophical materials in the Middle Ages.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "lisbon",
    place_name: "Lisbon",
    latitude: 38.7223,
    longitude: -9.1393,
    region: "Iberia",
    modern_name: "Lisbon, Portugal",
    alchemical_significance:
      "A major Iberian port that linked Latin, Arabic, and Mediterranean knowledge networks and later supported the circulation of chemical and alchemical texts.",
    key_periods: ["EARLY_MODERN"]
  },
  {
    slug: "madrid",
    place_name: "Madrid",
    latitude: 40.4168,
    longitude: -3.7038,
    region: "Iberia",
    modern_name: "Madrid, Spain",
    alchemical_significance:
      "A major Iberian political center that became important for learned exchange, courtly patronage, and the circulation of practical chemical knowledge.",
    key_periods: ["EARLY_MODERN"]
  },
  {
    slug: "monte-cassino",
    place_name: "Monte Cassino",
    latitude: 41.4917,
    longitude: 13.8116,
    region: "Italy",
    modern_name: "Cassino, Italy",
    alchemical_significance:
      "A foundational Benedictine monastic center where manuscript copying and scholarly exchange helped preserve scientific and medical learning.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "salerno",
    place_name: "Salerno",
    latitude: 40.6824,
    longitude: 14.7681,
    region: "Italy",
    modern_name: "Salerno, Italy",
    alchemical_significance:
      "A major medical center whose pharmacy, materia medica, and translation culture made it important for the development of practical alchemical knowledge.",
    key_periods: ["MEDIEVAL"]
  },
  {
    slug: "ven-island",
    place_name: "Venice",
    latitude: 45.4408,
    longitude: 12.3155,
    region: "Italy",
    modern_name: "Venice, Italy",
    alchemical_significance:
      "A printing and commercial hub that helped move alchemical books, pigments, glassware, and laboratory techniques across Europe.",
    aliases: ["venice"],
    key_periods: ["RENAISSANCE", "EARLY_MODERN"]
  }
];

const eraDefinitions = [
  {
    value: "ANTIQUITY",
    label: "Antiquity / Hellenistic",
    matches: (year) => year !== null && year < 300
  },
  {
    value: "LATE_ANTIQUE",
    label: "Late Antique",
    matches: (year) => year !== null && year >= 300 && year < 600
  },
  {
    value: "MEDIEVAL",
    label: "Medieval",
    matches: (year) => year !== null && year >= 600 && year < 1450
  },
  {
    value: "RENAISSANCE",
    label: "Renaissance",
    matches: (year) => year !== null && year >= 1450 && year < 1550
  },
  {
    value: "EARLY_MODERN",
    label: "Early Modern",
    matches: (year) => year !== null && year >= 1550 && year < 1700
  },
  {
    value: "ENLIGHTENMENT",
    label: "Enlightenment / Chemical Revolution",
    matches: (year) => year !== null && year >= 1700
  }
];

const filterState = {
  eras: new Set(),
  centuries: new Set(),
  themes: new Set()
};

let filterSummaryNode = null;
let filterCountsNode = null;
let centuryOptions = [];
let themeOptions = [];

function parseList(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (!value) {
    return [];
  }
  if (typeof value === "string") {
    try {
      const parsed = JSON.parse(value);
      return Array.isArray(parsed) ? parsed : [];
    } catch (error) {
      return value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    }
  }
  return [];
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function ordinal(n) {
  const mod100 = n % 100;
  if (mod100 >= 11 && mod100 <= 13) {
    return `${n}th`;
  }
  const mod10 = n % 10;
  if (mod10 === 1) return `${n}st`;
  if (mod10 === 2) return `${n}nd`;
  if (mod10 === 3) return `${n}rd`;
  return `${n}th`;
}

function getCenturyLabel(year) {
  if (year === null || Number.isNaN(year)) {
    return null;
  }
  const century = Math.floor(year / 100) + 1;
  return `${ordinal(century)} century`;
}

function getEraForYear(year) {
  const definition = eraDefinitions.find((entry) => entry.matches(year));
  return definition ? definition.value : null;
}

function getEraLabel(eraValue) {
  const definition = eraDefinitions.find((entry) => entry.value === eraValue);
  return definition ? definition.label : eraValue;
}

function getConceptLabel(slug) {
  if (!allData?.concepts) {
    return slug;
  }
  const concept = allData.concepts.find((entry) => entry.slug === slug);
  return concept ? concept.label : slug;
}

function getPersonBySlug(slug) {
  if (!allData?.persons) {
    return null;
  }
  return allData.persons.find((entry) => entry.slug === slug) || null;
}

function normalizeLocationSlug(slug) {
  const raw = (slug || "").trim();
  return locationAliases[raw] || raw;
}

function normalizeLocationRecord(location) {
  return {
    ...location,
    aliases: parseList(location.aliases),
    key_periods: parseList(location.key_periods),
    normalized_slug: normalizeLocationSlug(location.slug)
  };
}

function buildLocationIndex(data) {
  locationIndex = new Map();
  const sourceLocations = [...(data.locations || []), ...fallbackLocations];

  for (const location of sourceLocations) {
    if (!location || !location.slug) {
      continue;
    }

    const normalized = normalizeLocationRecord(location);
    locationIndex.set(normalized.slug, normalized);
    locationIndex.set(normalized.normalized_slug, normalized);

    for (const alias of normalized.aliases) {
      if (alias) {
        locationIndex.set(alias, normalized);
      }
    }
  }
}

function buildEventIndex(data) {
  eventsByLocation = new Map();

  for (const event of data.events || []) {
    const normalizedSlug = normalizeLocationSlug(event.location_slug);
    const enrichedEvent = {
      ...event,
      normalized_location_slug: normalizedSlug,
      persons_involved: parseList(event.persons_involved),
      texts_involved: parseList(event.texts_involved),
      concepts_involved: parseList(event.concepts_involved)
    };

    if (!eventsByLocation.has(normalizedSlug)) {
      eventsByLocation.set(normalizedSlug, []);
    }
    eventsByLocation.get(normalizedSlug).push(enrichedEvent);
  }

  for (const events of eventsByLocation.values()) {
    events.sort((left, right) => {
      const leftYear = Number.isFinite(left.date_start_year) ? left.date_start_year : 0;
      const rightYear = Number.isFinite(right.date_start_year) ? right.date_start_year : 0;
      if (leftYear !== rightYear) {
        return leftYear - rightYear;
      }
      return String(left.date_label || "").localeCompare(String(right.date_label || ""));
    });
  }
}

function getEventsForLocation(locationSlug) {
  const normalized = normalizeLocationSlug(locationSlug);
  return eventsByLocation.get(normalized) || [];
}

function buildFilterCatalog() {
  const centuries = new Map();
  const themes = new Map();

  for (const event of allData.events || []) {
    const year = Number.isFinite(event.date_start_year) ? event.date_start_year : null;
    const centuryLabel = getCenturyLabel(year);
    if (centuryLabel) {
      centuries.set(centuryLabel, (centuries.get(centuryLabel) || 0) + 1);
    }

    for (const themeSlug of parseList(event.concepts_involved)) {
      themes.set(themeSlug, (themes.get(themeSlug) || 0) + 1);
    }
  }

  centuryOptions = Array.from(centuries.entries())
    .sort((left, right) => {
      const leftValue = parseInt(left[0], 10);
      const rightValue = parseInt(right[0], 10);
      return leftValue - rightValue;
    })
    .map(([label, count]) => ({ value: label, label, count }));

  themeOptions = Array.from(themes.entries())
    .map(([slug, count]) => ({
      value: slug,
      label: getConceptLabel(slug),
      count
    }))
    .sort((left, right) => {
      if (right.count !== left.count) {
        return right.count - left.count;
      }
      return String(left.label).localeCompare(String(right.label));
    });
}

function eventMatchesFilters(event) {
  const year = Number.isFinite(event.date_start_year) ? event.date_start_year : null;
  const era = getEraForYear(year);
  const century = getCenturyLabel(year);
  const themes = new Set(parseList(event.concepts_involved));

  if (filterState.eras.size > 0 && (!era || !filterState.eras.has(era))) {
    return false;
  }

  if (filterState.centuries.size > 0 && (!century || !filterState.centuries.has(century))) {
    return false;
  }

  if (filterState.themes.size > 0) {
    let hasMatch = false;
    for (const themeSlug of themes) {
      if (filterState.themes.has(themeSlug)) {
        hasMatch = true;
        break;
      }
    }
    if (!hasMatch) {
      return false;
    }
  }

  return true;
}

function getMatchingEvents(locationSlug) {
  return getEventsForLocation(locationSlug).filter(eventMatchesFilters);
}

function stripHtml(html) {
  const container = document.createElement("div");
  container.innerHTML = html || "";
  return container.textContent || container.innerText || "";
}

function truncateText(text, length) {
  if (text.length <= length) {
    return text;
  }
  return `${text.slice(0, length - 1).trim()}...`;
}

function buildEventSummary(event) {
  const description = stripHtml(event.description || "");
  if (!description) {
    return "";
  }
  return truncateText(description.replace(/\s+/g, " ").trim(), 180);
}

function buildEventItem(event) {
  const concepts = event.concepts_involved
    .slice(0, 3)
    .map((slug) => getConceptLabel(slug))
    .filter(Boolean);

  return `
    <li class="event-card">
      <div class="event-card__date">${escapeHtml(event.date_label || "Undated")}</div>
      ${event.description ? `<div class="event-card__summary">${escapeHtml(buildEventSummary(event))}</div>` : ""}
      ${concepts.length > 0 ? `<div class="event-card__tags">${concepts.map((label) => `<span class="event-tag">${escapeHtml(label)}</span>`).join("")}</div>` : ""}
    </li>
  `;
}

function buildLocationPopup(location, events) {
  const allEvents = getEventsForLocation(location.slug);
  const keyFigures = parseList(location.key_figures || []);
  const keyPeriods = parseList(location.key_periods || []);

  let popupHtml = `
    <div class="location-popup">
      <h3>${escapeHtml(location.place_name)}</h3>
      <p class="location-popup__meta">
        <strong>Modern name:</strong> ${escapeHtml(location.modern_name || "")}<br>
        <strong>Region:</strong> ${escapeHtml(location.region || "")}
      </p>
      <div class="location-popup__significance">
        <strong>Alchemical significance:</strong><br>
        ${escapeHtml(location.alchemical_significance || "")}
      </div>
  `;

  if (keyPeriods.length > 0) {
    popupHtml += `
      <p class="location-popup__periods">
        <strong>Key periods:</strong> ${keyPeriods.map((period) => escapeHtml(period.replace(/_/g, " "))).join(", ")}
      </p>
    `;
  }

  if (keyFigures.length > 0) {
    popupHtml += `
      <div class="location-popup__figures">
        <strong>Key figures:</strong>
        <ul>
          ${keyFigures
            .map((slug) => {
              const person = getPersonBySlug(slug);
              if (!person) {
                return "";
              }
              return `<li><a href="../persons/${escapeHtml(slug)}.html">${escapeHtml(person.name)}</a></li>`;
            })
            .join("")}
        </ul>
      </div>
    `;
  }

  popupHtml += `
      <div class="location-popup__events">
        <strong>Events at this location:</strong> ${allEvents.length}
  `;

  if (filterState.eras.size > 0 || filterState.centuries.size > 0 || filterState.themes.size > 0) {
    popupHtml += `<div class="location-popup__filter-note">${events.length} event(s) match the active filters here.</div>`;
  }

  if (events.length > 0) {
    popupHtml += `
        <ul class="location-event-list">
          ${events.map(buildEventItem).join("")}
        </ul>
      </div>
    `;
  } else {
    popupHtml += `
        <p><em>No events match the active filters at this location.</em></p>
      </div>
    `;
  }

  popupHtml += `</div>`;
  return popupHtml;
}

function buildTooltip(location, events) {
  return `
    <strong>${escapeHtml(location.place_name)}</strong><br>
    ${events.length} filtered event${events.length === 1 ? "" : "s"}
  `;
}

function createLocationMarker(location) {
  const color = regionColors[location.region] || "#808080";
  const events = getEventsForLocation(location.slug);

  const icon = L.divIcon({
    html: `<div style="background-color: ${color}; border: 2px solid white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">&#9679;</div>`,
    className: "location-marker",
    iconSize: [24, 24],
    iconAnchor: [12, 12]
  });

  const marker = L.marker([location.latitude, location.longitude], { icon });

  marker.bindTooltip(buildTooltip(location, events), {
    permanent: false,
    direction: "top",
    offset: [0, -10],
    className: "location-tooltip"
  });

  marker.bindPopup(buildLocationPopup(location, events), {
    maxWidth: 460,
    minWidth: 320,
    className: "location-popup-container"
  });

  marker.addTo(map);
  locationMarkers[location.slug] = {
    marker,
    location
  };
}

function updateMarkerState(locationSlug) {
  const entry = locationMarkers[locationSlug];
  if (!entry) {
    return;
  }

  const { marker, location } = entry;
  const matchingEvents = getMatchingEvents(location.slug);
  const totalEvents = getEventsForLocation(location.slug).length;
  const hasVisibleEvents = matchingEvents.length > 0;

  marker.setOpacity(hasVisibleEvents ? 1 : 0.18);

  if (typeof marker.setTooltipContent === "function") {
    marker.setTooltipContent(buildTooltip(location, matchingEvents));
  } else {
    marker.unbindTooltip();
    marker.bindTooltip(buildTooltip(location, matchingEvents), {
      permanent: false,
      direction: "top",
      offset: [0, -10],
      className: "location-tooltip"
    });
  }

  if (typeof marker.setPopupContent === "function") {
    marker.setPopupContent(buildLocationPopup(location, matchingEvents));
  } else {
    marker.unbindPopup();
    marker.bindPopup(buildLocationPopup(location, matchingEvents), {
      maxWidth: 460,
      minWidth: 320,
      className: "location-popup-container"
    });
  }

  if (marker._icon) {
    marker._icon.style.filter = hasVisibleEvents ? "none" : "grayscale(0.4)";
  }

  return {
    visible: hasVisibleEvents,
    totalEvents,
    matchingEvents: matchingEvents.length
  };
}

function applyFilters() {
  let visibleLocations = 0;
  let visibleEvents = 0;

  Object.keys(locationMarkers).forEach((slug) => {
    const stats = updateMarkerState(slug);
    if (stats) {
      if (stats.visible) {
        visibleLocations += 1;
      }
      visibleEvents += stats.matchingEvents;
    }
  });

  updateFilterSummary(visibleLocations, visibleEvents);
}

function updateFilterSummary(visibleLocations, visibleEvents) {
  if (filterSummaryNode) {
    const filtersActive =
      filterState.eras.size > 0 || filterState.centuries.size > 0 || filterState.themes.size > 0;
    filterSummaryNode.innerHTML = filtersActive
      ? `Showing <strong>${visibleLocations}</strong> location(s) and <strong>${visibleEvents}</strong> event(s) that match the active filters.`
      : `Showing all <strong>${visibleLocations}</strong> location(s) and <strong>${visibleEvents}</strong> event(s).`;
  }

  if (filterCountsNode) {
    filterCountsNode.textContent = `${visibleEvents} matching events`;
  }
}

function syncFilterStateFromControls(container) {
  filterState.eras.clear();
  filterState.centuries.clear();
  filterState.themes.clear();

  container.querySelectorAll('input[data-filter-kind="era"]:checked').forEach((input) => {
    filterState.eras.add(input.value);
  });

  container.querySelectorAll('input[data-filter-kind="century"]:checked').forEach((input) => {
    filterState.centuries.add(input.value);
  });

  container.querySelectorAll('input[data-filter-kind="theme"]:checked').forEach((input) => {
    filterState.themes.add(input.value);
  });
}

function renderFilterSection(title, items, kind) {
  const inputs = items
    .map(
      (item) => `
        <label class="filter-option">
          <input type="checkbox" data-filter-kind="${kind}" value="${escapeHtml(item.value)}">
          <span>${escapeHtml(item.label)} <em>(${item.count})</em></span>
        </label>
      `
    )
    .join("");

  return `
    <details class="filter-group" open>
      <summary>${escapeHtml(title)}</summary>
      <div class="filter-group__body">
        ${inputs}
      </div>
    </details>
  `;
}

function addFilterControl() {
  const control = L.control({ position: "topleft" });

  control.onAdd = function () {
    const container = L.DomUtil.create("div", "map-filter-control");
    container.innerHTML = `
      <div class="map-filter-panel">
        <div class="map-filter-panel__header">
          <div>
            <h4>Explore the map</h4>
            <p>Leave a section empty to keep it unconstrained.</p>
          </div>
          <button type="button" class="map-filter-reset" data-action="reset-filters">Reset</button>
        </div>
        ${renderFilterSection(
          "Era",
          eraDefinitions.map((entry) => ({
            value: entry.value,
            label: entry.label,
            count: allData.events.filter((event) => getEraForYear(Number.isFinite(event.date_start_year) ? event.date_start_year : null) === entry.value).length
          })),
          "era"
        )}
        ${renderFilterSection("Century", centuryOptions, "century")}
        ${renderFilterSection("Theme", themeOptions, "theme")}
        <div class="map-filter-panel__summary" data-role="filter-summary"></div>
        <div class="map-filter-panel__counts" data-role="filter-counts"></div>
      </div>
    `;

    L.DomEvent.disableClickPropagation(container);
    L.DomEvent.disableScrollPropagation(container);

    container.addEventListener("change", (event) => {
      const target = event.target;
      if (target && target.matches('input[type="checkbox"][data-filter-kind]')) {
        syncFilterStateFromControls(container);
        applyFilters();
      }
    });

    container.addEventListener("click", (event) => {
      const button = event.target.closest('[data-action="reset-filters"]');
      if (!button) {
        return;
      }

      container.querySelectorAll('input[type="checkbox"][data-filter-kind]').forEach((input) => {
        input.checked = false;
      });
      syncFilterStateFromControls(container);
      applyFilters();
    });

    filterSummaryNode = container.querySelector('[data-role="filter-summary"]');
    filterCountsNode = container.querySelector('[data-role="filter-counts"]');

    return container;
  };

  control.addTo(map);
}

function addLegend() {
  const legend = L.control({ position: "bottomright" });

  legend.onAdd = function () {
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML = `
      <div style="background: white; padding: 12px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,0,0,0.2); max-height: 300px; overflow-y: auto;">
        <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #333;">Regions</h4>
        <div style="font-size: 12px;">
          ${Object.entries(regionColors)
            .map(
              ([region, color]) => `
                <div style="margin: 5px 0; display: flex; align-items: center;">
                  <span style="display: inline-block; width: 16px; height: 16px; background-color: ${color}; border-radius: 50%; margin-right: 8px; border: 1px solid #ddd;"></span>
                  ${escapeHtml(region)}
                </div>
              `
            )
            .join("")}
        </div>
        <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
        <h4 style="margin: 10px 0 5px 0; font-size: 12px; color: #666;">
          <strong>Total Events:</strong> ${allData.events.length}
        </h4>
      </div>
    `;
    return div;
  };

  legend.addTo(map);
}

function addMapStyles() {
  const style = document.createElement("style");
  style.textContent = `
    .location-tooltip {
      background-color: #333 !important;
      color: white !important;
      border-radius: 4px !important;
      padding: 6px 10px !important;
      font-size: 12px !important;
      font-weight: 500 !important;
      border: none !important;
    }

    .location-popup-container .leaflet-popup-content {
      margin: 0 !important;
      padding: 0 !important;
    }

    .location-popup {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      color: #333;
      max-width: 420px;
    }

    .location-popup h3 {
      margin: 0 0 10px 0;
      color: #111;
      font-size: 16px;
      border-bottom: 2px solid #888;
      padding-bottom: 8px;
    }

    .location-popup__meta,
    .location-popup__periods {
      margin: 8px 0;
      font-size: 12px;
      color: #555;
    }

    .location-popup__significance {
      margin: 10px 0;
      padding: 8px;
      background-color: #f9f9f9;
      border-left: 3px solid #888;
      font-size: 13px;
    }

    .location-popup__figures,
    .location-popup__events {
      margin: 10px 0;
      font-size: 13px;
    }

    .location-popup__figures ul,
    .location-event-list {
      margin: 6px 0 0 0;
      padding-left: 18px;
    }

    .location-popup__filter-note {
      margin-top: 6px;
      font-size: 12px;
      color: #666;
      font-style: italic;
    }

    .location-event-list {
      max-height: 260px;
      overflow-y: auto;
    }

    .event-card {
      margin-bottom: 10px;
      padding-bottom: 10px;
      border-bottom: 1px solid #eee;
    }

    .event-card__date {
      font-size: 12px;
      font-weight: 700;
      color: #222;
      margin-bottom: 4px;
    }

    .event-card__summary {
      font-size: 12px;
      line-height: 1.45;
      color: #444;
    }

    .event-card__tags {
      margin-top: 5px;
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }

    .event-tag {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 999px;
      background: #f0f0f0;
      font-size: 11px;
      color: #444;
    }

    .map-filter-control {
      z-index: 400;
      max-width: 320px;
    }

    .map-filter-panel {
      background: white;
      padding: 12px;
      border-radius: 8px;
      box-shadow: 0 0 15px rgba(0,0,0,0.2);
      width: 320px;
      max-height: 78vh;
      overflow-y: auto;
      font-size: 12px;
    }

    .map-filter-panel__header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }

    .map-filter-panel__header h4 {
      margin: 0;
      font-size: 14px;
      color: #222;
    }

    .map-filter-panel__header p {
      margin: 4px 0 0 0;
      color: #666;
      line-height: 1.35;
    }

    .map-filter-reset {
      border: 1px solid #ccc;
      background: #fafafa;
      color: #222;
      border-radius: 6px;
      padding: 6px 10px;
      cursor: pointer;
      font-size: 12px;
    }

    .map-filter-reset:hover {
      background: #f2f2f2;
    }

    .filter-group {
      margin: 8px 0;
      border: 1px solid #eee;
      border-radius: 6px;
      padding: 8px;
      background: #fcfcfc;
    }

    .filter-group summary {
      cursor: pointer;
      font-weight: 600;
      color: #333;
    }

    .filter-group__body {
      margin-top: 8px;
      display: grid;
      gap: 6px;
      max-height: 150px;
      overflow-y: auto;
    }

    .filter-option {
      display: flex;
      gap: 8px;
      align-items: flex-start;
      line-height: 1.35;
      color: #333;
    }

    .filter-option input {
      margin-top: 2px;
    }

    .map-filter-panel__summary,
    .map-filter-panel__counts {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid #eee;
      color: #333;
      line-height: 1.4;
    }
  `;
  document.head.appendChild(style);
}

async function loadAndDisplayData() {
  try {
    const response = await fetch("data/data.json");
    if (!response.ok) {
      throw new Error(`Unable to load data.json (${response.status})`);
    }

    allData = await response.json();
    buildLocationIndex(allData);
    buildEventIndex(allData);
    buildFilterCatalog();

    for (const location of locationIndex.values()) {
      if (locationMarkers[location.slug]) {
        continue;
      }
      createLocationMarker(location);
    }

    addFilterControl();
    addLegend();
    applyFilters();
  } catch (error) {
    console.error("Failed to load map data:", error);
    const mapContainer = document.getElementById("map");
    if (mapContainer) {
      mapContainer.innerHTML = `
        <div style="padding: 24px; background: #fff7f7; border: 1px solid #f1c0c0; color: #7a1f1f; border-radius: 8px;">
          <strong>Map data could not load.</strong><br>
          ${escapeHtml(error.message || "Unknown error")}
        </div>
      `;
    }
  }
}

function initMap() {
  map = L.map("map").setView([35, 15], 4);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
    maxZoom: 19,
    minZoom: 2
  }).addTo(map);

  addMapStyles();
  loadAndDisplayData();
}

document.addEventListener("DOMContentLoaded", initMap);
