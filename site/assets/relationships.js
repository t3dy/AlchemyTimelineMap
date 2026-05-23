/**
 * ALCHEMYTIMELINEMAP Relationship Lookups
 * Provides functions to find related entities (concepts, texts, persons, events)
 */

class Relationships {
  constructor(data) {
    this.data = data;
    this.relationships = data.relationships || {};
    this.persons = {};
    this.texts = {};
    this.concepts = {};
    this.events = {};

    // Build lookup maps
    (data.persons || []).forEach(p => this.persons[p.slug] = p);
    (data.texts || []).forEach(t => this.texts[t.slug] = t);
    (data.concepts || []).forEach(c => this.concepts[c.slug] = c);
    (data.events || []).forEach(e => this.events[e.slug] = e);
  }

  /**
   * Get concepts related to a person
   */
  getPersonConcepts(personSlug) {
    const conceptSlugs = this.relationships.person_to_concepts?.[personSlug] || [];
    return conceptSlugs.map(slug => this.concepts[slug]).filter(c => c);
  }

  /**
   * Get texts related to a person
   */
  getPersonTexts(personSlug) {
    const textSlugs = this.relationships.person_to_texts?.[personSlug] || [];
    return textSlugs.map(slug => this.texts[slug]).filter(t => t);
  }

  /**
   * Get events related to a person
   */
  getPersonEvents(personSlug) {
    const eventSlugs = this.relationships.person_to_events?.[personSlug] || [];
    return eventSlugs.map(slug => this.events[slug]).filter(e => e);
  }

  /**
   * Get persons related to a concept
   */
  getConceptPersons(conceptSlug) {
    const personSlugs = this.relationships.concept_to_persons?.[conceptSlug] || [];
    return personSlugs.map(slug => this.persons[slug]).filter(p => p);
  }

  /**
   * Get texts related to a concept
   */
  getConceptTexts(conceptSlug) {
    const textSlugs = this.relationships.concept_to_texts?.[conceptSlug] || [];
    return textSlugs.map(slug => this.texts[slug]).filter(t => t);
  }

  /**
   * Get events related to a concept
   */
  getConceptEvents(conceptSlug) {
    const eventSlugs = this.relationships.concept_to_events?.[conceptSlug] || [];
    return eventSlugs.map(slug => this.events[slug]).filter(e => e);
  }

  /**
   * Get concepts related to a text
   */
  getTextConcepts(textSlug) {
    const conceptSlugs = this.relationships.text_to_concepts?.[textSlug] || [];
    return conceptSlugs.map(slug => this.concepts[slug]).filter(c => c);
  }

  /**
   * Get persons related to a text
   */
  getTextPersons(textSlug) {
    const personSlugs = this.relationships.text_to_persons?.[textSlug] || [];
    return personSlugs.map(slug => this.persons[slug]).filter(p => p);
  }
}

// Global relationships instance
window.relationshipsService = null;

// Load relationships on page load
document.addEventListener('DOMContentLoaded', () => {
  fetch('data/data.json')
    .then(response => response.json())
    .then(data => {
      window.relationshipsService = new Relationships(data);
      // Trigger relationship population if the script exists on the page
      if (typeof populateEntityRelationships === 'function') {
        populateEntityRelationships();
      }
    })
    .catch(error => console.error('Failed to load relationships data:', error));
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Relationships;
}
