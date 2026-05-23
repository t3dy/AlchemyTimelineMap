/**
 * ALCHEMYTIMELINEMAP Global Filter State Management
 * Manages concept, era, and person filters across timeline, map, and other views
 */

class FilterState {
  constructor() {
    this.concepts = [];
    this.eras = [];
    this.persons = [];
    this.listeners = [];
    this.loadFromStorage();
  }

  /**
   * Load filter state from localStorage
   */
  loadFromStorage() {
    try {
      const stored = localStorage.getItem('alchemy-filters');
      if (stored) {
        const data = JSON.parse(stored);
        this.concepts = data.concepts || [];
        this.eras = data.eras || [];
        this.persons = data.persons || [];
      }
    } catch (e) {
      console.warn('Failed to load filters from storage:', e);
    }
  }

  /**
   * Save filter state to localStorage
   */
  saveToStorage() {
    try {
      localStorage.setItem('alchemy-filters', JSON.stringify({
        concepts: this.concepts,
        eras: this.eras,
        persons: this.persons,
      }));
    } catch (e) {
      console.warn('Failed to save filters to storage:', e);
    }
  }

  /**
   * Set concept filter (array of slugs)
   */
  setConceptFilter(conceptSlugs) {
    this.concepts = conceptSlugs || [];
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Set era filter (array of era slugs: LATE_ANTIQUE, MEDIEVAL, EARLY_MODERN)
   */
  setEraFilter(eraSlugs) {
    this.eras = eraSlugs || [];
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Set person filter (array of person slugs)
   */
  setPersonFilter(personSlugs) {
    this.persons = personSlugs || [];
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Toggle concept in filter
   */
  toggleConcept(conceptSlug) {
    const idx = this.concepts.indexOf(conceptSlug);
    if (idx > -1) {
      this.concepts.splice(idx, 1);
    } else {
      this.concepts.push(conceptSlug);
    }
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Toggle era in filter
   */
  toggleEra(eraSlug) {
    const idx = this.eras.indexOf(eraSlug);
    if (idx > -1) {
      this.eras.splice(idx, 1);
    } else {
      this.eras.push(eraSlug);
    }
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Toggle person in filter
   */
  togglePerson(personSlug) {
    const idx = this.persons.indexOf(personSlug);
    if (idx > -1) {
      this.persons.splice(idx, 1);
    } else {
      this.persons.push(personSlug);
    }
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Clear all filters
   */
  clearFilters() {
    this.concepts = [];
    this.eras = [];
    this.persons = [];
    this.saveToStorage();
    this.notifyListeners();
  }

  /**
   * Check if any filters are active
   */
  hasActiveFilters() {
    return this.concepts.length > 0 || this.eras.length > 0 || this.persons.length > 0;
  }

  /**
   * Check if an entity matches current filters
   * @param {Object} entity - timeline event or other entity
   * @param {Array} entityConcepts - concept slugs associated with entity
   * @param {Array} entityPersons - person slugs associated with entity
   * @param {string} entityEra - era slug of entity
   * @returns {boolean} true if entity passes filters
   */
  matchesFilters(entity) {
    // No filters = match all
    if (!this.hasActiveFilters()) {
      return true;
    }

    const conceptTags = entity.concepts_involved ?
      entity.concepts_involved.split(';').map(c => c.trim()) : [];
    const personTags = entity.persons_involved ?
      entity.persons_involved.split(';').map(p => p.trim()) : [];
    const era = entity.era || '';

    // Concept filter: entity must have at least one matching concept
    if (this.concepts.length > 0) {
      const hasMatchingConcept = this.concepts.some(c => conceptTags.includes(c));
      if (!hasMatchingConcept) return false;
    }

    // Era filter: entity's era must match one of selected eras
    if (this.eras.length > 0) {
      if (!this.eras.includes(era)) return false;
    }

    // Person filter: entity must involve at least one matching person
    if (this.persons.length > 0) {
      const hasMatchingPerson = this.persons.some(p => personTags.includes(p));
      if (!hasMatchingPerson) return false;
    }

    return true;
  }

  /**
   * Register a listener to be called when filters change
   */
  onFilterChange(callback) {
    this.listeners.push(callback);
  }

  /**
   * Notify all listeners of filter change
   */
  notifyListeners() {
    this.listeners.forEach(callback => {
      try {
        callback(this);
      } catch (e) {
        console.error('Filter listener error:', e);
      }
    });
  }

  /**
   * Get all active filters as a display string
   */
  getActiveFilterString() {
    const parts = [];
    if (this.concepts.length > 0) {
      parts.push(`${this.concepts.length} concept(s)`);
    }
    if (this.eras.length > 0) {
      parts.push(`${this.eras.length} era(s)`);
    }
    if (this.persons.length > 0) {
      parts.push(`${this.persons.length} person(s)`);
    }
    return parts.length > 0 ? parts.join(', ') : 'No filters';
  }
}

// Global filter state instance
window.filterState = new FilterState();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FilterState;
}
