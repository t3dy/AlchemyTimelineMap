/**
 * ALCHEMYTIMELINEMAP Timeline Viewer
 * Renders and filters 582 timeline events by era, concept, and person
 */

class TimelineViewer {
  constructor(containerId, dataPath = 'data/data.json') {
    this.containerId = containerId;
    this.dataPath = dataPath;
    this.data = null;
    this.allEvents = [];
    this.eraOrder = ['LATE_ANTIQUE', 'MEDIEVAL', 'EARLY_MODERN'];
    this.eraLabels = {
      'LATE_ANTIQUE': 'Late Antiquity (3rd–7th centuries)',
      'MEDIEVAL': 'Medieval (7th–15th centuries)',
      'EARLY_MODERN': 'Early Modern (15th–18th centuries)',
    };
  }

  /**
   * Initialize timeline: load data and render
   */
  async init() {
    try {
      const response = await fetch(this.dataPath);
      if (!response.ok) throw new Error(`Failed to load ${this.dataPath}`);
      this.data = await response.json();
      this.allEvents = this.data.events || [];
      this.render();
      this.setupFilterUI();
      this.attachFilterListeners();
    } catch (error) {
      console.error('Timeline initialization error:', error);
      this.showError(error.message);
    }
  }

  /**
   * Setup filter UI: populate concept/person lists, attach event handlers
   */
  setupFilterUI() {
    // Collect all concepts and persons from events
    const conceptSet = new Set();
    const personSet = new Set();

    this.allEvents.forEach(event => {
      if (event.concepts_involved) {
        event.concepts_involved.split(';').forEach(c => {
          const slug = c.trim();
          if (slug) conceptSet.add(slug);
        });
      }
      if (event.persons_involved) {
        event.persons_involved.split(';').forEach(p => {
          const slug = p.trim();
          if (slug) personSet.add(slug);
        });
      }
    });

    // Populate concept filter options
    const conceptContainer = document.getElementById('concept-filter-options');
    if (conceptContainer) {
      const concepts = Array.from(conceptSet).sort();
      concepts.forEach(concept => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.value = concept;
        input.addEventListener('change', (e) => {
          if (e.target.checked) {
            window.filterState.toggleConcept(concept);
          } else {
            window.filterState.toggleConcept(concept);
          }
        });
        label.appendChild(input);
        label.appendChild(document.createTextNode(concept));
        label.className = 'filter-checkbox-label';
        conceptContainer.appendChild(label);
      });
    }

    // Populate person filter options
    const personContainer = document.getElementById('person-filter-options');
    if (personContainer) {
      const persons = Array.from(personSet).sort();
      persons.forEach(person => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.value = person;
        input.addEventListener('change', (e) => {
          if (e.target.checked) {
            window.filterState.togglePerson(person);
          } else {
            window.filterState.togglePerson(person);
          }
        });
        label.appendChild(input);
        label.appendChild(document.createTextNode(person));
        label.className = 'filter-checkbox-label';
        personContainer.appendChild(label);
      });
    }

    // Setup era filter handlers
    const eraCheckboxes = document.querySelectorAll('input[data-era]');
    eraCheckboxes.forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        const eras = Array.from(eraCheckboxes)
          .filter(cb => cb.checked)
          .map(cb => cb.getAttribute('data-era'));
        window.filterState.setEraFilter(eras);
      });
    });

    // Setup clear filters button
    const clearBtn = document.getElementById('clear-filters-btn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        // Clear all checkboxes
        eraCheckboxes.forEach(cb => cb.checked = false);
        document.querySelectorAll('#concept-filter-options input').forEach(cb => cb.checked = false);
        document.querySelectorAll('#person-filter-options input').forEach(cb => cb.checked = false);
        // Clear search inputs
        const conceptSearch = document.getElementById('concept-search');
        const personSearch = document.getElementById('person-search');
        if (conceptSearch) conceptSearch.value = '';
        if (personSearch) personSearch.value = '';
        // Clear filter state
        window.filterState.clearFilters();
      });
    }

    // Setup search input handlers
    const conceptSearch = document.getElementById('concept-search');
    if (conceptSearch) {
      conceptSearch.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const checkboxes = document.querySelectorAll('#concept-filter-options label');
        checkboxes.forEach(label => {
          const text = label.textContent.toLowerCase();
          label.style.display = text.includes(query) ? '' : 'none';
        });
      });
    }

    const personSearch = document.getElementById('person-search');
    if (personSearch) {
      personSearch.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const checkboxes = document.querySelectorAll('#person-filter-options label');
        checkboxes.forEach(label => {
          const text = label.textContent.toLowerCase();
          label.style.display = text.includes(query) ? '' : 'none';
        });
      });
    }
  }

  /**
   * Render timeline with all events
   */
  render() {
    const container = document.getElementById(this.containerId);
    if (!container) {
      console.error(`Timeline container not found: ${this.containerId}`);
      return;
    }

    container.innerHTML = '';

    // Group events by era
    const eventsByEra = {};
    this.eraOrder.forEach(era => {
      eventsByEra[era] = [];
    });

    this.allEvents.forEach(event => {
      const era = event.era || 'MEDIEVAL';
      if (eventsByEra[era]) {
        eventsByEra[era].push(event);
      }
    });

    // Sort events within each era by start date
    Object.keys(eventsByEra).forEach(era => {
      eventsByEra[era].sort((a, b) => {
        const aDate = parseInt(a.date_start_year) || 0;
        const bDate = parseInt(b.date_start_year) || 0;
        return aDate - bDate;
      });
    });

    // Create era sections
    this.eraOrder.forEach(era => {
      if (eventsByEra[era].length === 0) return;

      const section = document.createElement('div');
      section.className = 'era-section';
      section.setAttribute('data-era', era);

      const heading = document.createElement('h3');
      heading.textContent = this.eraLabels[era];
      section.appendChild(heading);

      const eventCount = document.createElement('p');
      eventCount.className = 'era-event-count';
      eventCount.textContent = `${eventsByEra[era].length} events`;
      section.appendChild(eventCount);

      const eventsContainer = document.createElement('div');
      eventsContainer.className = 'era-events';

      eventsByEra[era].forEach(event => {
        const card = this.createEventCard(event);
        eventsContainer.appendChild(card);
      });

      section.appendChild(eventsContainer);
      container.appendChild(section);
    });

    // Add initial filter count
    this.updateFilterCount();
  }

  /**
   * Create an event card element
   */
  createEventCard(event) {
    const card = document.createElement('div');
    card.className = 'event-card';
    card.setAttribute('data-slug', event.slug);
    card.setAttribute('data-era', event.era || 'MEDIEVAL');

    // Store filter-relevant data in data attributes
    if (event.concepts_involved) {
      card.setAttribute('data-concepts', event.concepts_involved);
    }
    if (event.persons_involved) {
      card.setAttribute('data-persons', event.persons_involved);
    }

    // Date badge
    const dateEl = document.createElement('div');
    dateEl.className = 'event-date';
    dateEl.textContent = this.formatDate(event);
    card.appendChild(dateEl);

    // Location (if available)
    if (event.location_slug) {
      const locEl = document.createElement('div');
      locEl.className = 'event-location';
      locEl.textContent = event.location_slug.replace(/-/g, ' ').toUpperCase();
      card.appendChild(locEl);
    }

    // Title
    const titleEl = document.createElement('h4');
    titleEl.className = 'event-title';
    titleEl.textContent = event.title || '(Untitled)';
    card.appendChild(titleEl);

    // Description (with converted HTML links)
    if (event.description_html) {
      const descEl = document.createElement('div');
      descEl.className = 'event-description';
      descEl.innerHTML = event.description_html;
      card.appendChild(descEl);
    }

    // Meta tags (concepts, persons)
    const metaEl = document.createElement('div');
    metaEl.className = 'event-meta-tags';

    if (event.concepts_involved) {
      const concepts = event.concepts_involved.split(';').map(c => c.trim());
      concepts.forEach(concept => {
        if (concept) {
          const tag = document.createElement('span');
          tag.className = 'meta-tag concept-tag';
          tag.textContent = concept;
          metaEl.appendChild(tag);
        }
      });
    }

    if (event.persons_involved) {
      const persons = event.persons_involved.split(';').map(p => p.trim());
      persons.forEach(person => {
        if (person) {
          const tag = document.createElement('span');
          tag.className = 'meta-tag person-tag';
          tag.textContent = person;
          metaEl.appendChild(tag);
        }
      });
    }

    if (metaEl.children.length > 0) {
      card.appendChild(metaEl);
    }

    return card;
  }

  /**
   * Format date for display
   */
  formatDate(event) {
    const year = event.date_start_year;
    if (!year) return 'Date unknown';

    const numYear = parseInt(year);
    const suffix = numYear < 0 ? ' BCE' : ' CE';
    return Math.abs(numYear) + suffix;
  }

  /**
   * Attach filter change listeners
   */
  attachFilterListeners() {
    if (typeof window.filterState !== 'undefined') {
      window.filterState.onFilterChange(() => this.applyFilters());
    }
  }

  /**
   * Apply current filters to timeline
   */
  applyFilters() {
    const cards = document.querySelectorAll('.event-card');
    let visibleCount = 0;
    let totalCount = cards.length;

    cards.forEach(card => {
      const event = {
        concepts_involved: card.getAttribute('data-concepts') || '',
        persons_involved: card.getAttribute('data-persons') || '',
        era: card.getAttribute('data-era') || 'MEDIEVAL',
      };

      if (window.filterState.matchesFilters(event)) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    this.updateFilterCount(visibleCount, totalCount);
  }

  /**
   * Update the filter count display
   */
  updateFilterCount(visibleCount = null, totalCount = null) {
    let countEl = document.getElementById('timeline-event-count');

    if (!countEl) {
      countEl = document.createElement('p');
      countEl.id = 'timeline-event-count';
      countEl.className = 'timeline-info';
      const header = document.querySelector('main > section');
      if (header) {
        header.insertBefore(countEl, header.querySelector('#timeline-container'));
      }
    }

    if (visibleCount === null) {
      visibleCount = this.allEvents.length;
      totalCount = this.allEvents.length;
    }

    const filterText = window.filterState && window.filterState.hasActiveFilters()
      ? ` (filtering by ${window.filterState.getActiveFilterString()})`
      : '';

    countEl.textContent = `Showing ${visibleCount} of ${totalCount} events${filterText}`;
  }

  /**
   * Show error message
   */
  showError(message) {
    const container = document.getElementById(this.containerId);
    if (container) {
      container.innerHTML = `<p class="error-message">Error loading timeline: ${message}</p>`;
    }
  }
}

// Initialize timeline when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const timeline = new TimelineViewer('timeline-container');
  timeline.init();
  window.timelineViewer = timeline; // Expose for debugging
});
