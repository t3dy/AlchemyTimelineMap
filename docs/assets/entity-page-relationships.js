/**
 * ALCHEMYTIMELINEMAP Entity Page Relationships
 * Populates "Related Concepts", "Related Persons", "Related Texts" sections on entity pages
 */

/**
 * Detect entity type and slug from page URL or DOM
 */
function detectEntityContext() {
  const path = window.location.pathname;

  if (path.includes('/persons/')) {
    const match = path.match(/\/persons\/([^/]+)\.html/);
    return { type: 'person', slug: match ? match[1] : null };
  } else if (path.includes('/texts/')) {
    const match = path.match(/\/texts\/([^/]+)\.html/);
    return { type: 'text', slug: match ? match[1] : null };
  } else if (path.includes('/concepts/')) {
    const match = path.match(/\/concepts\/([^/]+)\.html/);
    return { type: 'concept', slug: match ? match[1] : null };
  }

  return { type: null, slug: null };
}

/**
 * Create a card element for a related entity
 */
function createEntityCard(entity, entityType) {
  const card = document.createElement('div');
  card.className = 'entity-card';

  let title = '';
  let href = '';
  let meta = '';

  if (entityType === 'person') {
    title = entity.name;
    href = `../persons/${entity.slug}.html`;
    meta = `${entity.role_primary || 'Unknown'} | ${entity.era || 'Unknown era'}`;
  } else if (entityType === 'text') {
    title = entity.title;
    href = `../texts/${entity.slug}.html`;
    meta = `${entity.text_type || 'Unknown'} | ${entity.composition_date || 'Unknown date'}`;
  } else if (entityType === 'concept') {
    title = entity.label;
    href = `../concepts/${entity.slug}.html`;
    meta = entity.category_type || 'Concept';
  }

  const titleEl = document.createElement('div');
  titleEl.className = 'card-title';
  const linkEl = document.createElement('a');
  linkEl.href = href;
  linkEl.className = 'card-link';
  linkEl.textContent = title;
  titleEl.appendChild(linkEl);
  card.appendChild(titleEl);

  if (meta) {
    const metaEl = document.createElement('div');
    metaEl.className = 'card-meta';
    metaEl.textContent = meta;
    card.appendChild(metaEl);
  }

  return card;
}

/**
 * Populate relationship sections for a person
 */
function populatePersonRelationships(personSlug) {
  if (!window.relationshipsService) return;

  // Related Concepts
  const relatedConceptsContainer = document.getElementById('related-concepts');
  if (relatedConceptsContainer) {
    const concepts = window.relationshipsService.getPersonConcepts(personSlug);
    if (concepts.length > 0) {
      relatedConceptsContainer.innerHTML = '<h3>Related Concepts</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      concepts.forEach(concept => {
        grid.appendChild(createEntityCard(concept, 'concept'));
      });
      relatedConceptsContainer.appendChild(grid);
    } else {
      relatedConceptsContainer.innerHTML = '<p style="color: #999;">No related concepts.</p>';
    }
  }

  // Related Texts
  const relatedTextsContainer = document.getElementById('related-texts');
  if (relatedTextsContainer) {
    const texts = window.relationshipsService.getPersonTexts(personSlug);
    if (texts.length > 0) {
      relatedTextsContainer.innerHTML = '<h3>Related Texts</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      texts.forEach(text => {
        grid.appendChild(createEntityCard(text, 'text'));
      });
      relatedTextsContainer.appendChild(grid);
    } else {
      relatedTextsContainer.innerHTML = '<p style="color: #999;">No related texts.</p>';
    }
  }

  // Related Events
  const relatedEventsContainer = document.getElementById('related-events');
  if (relatedEventsContainer) {
    const events = window.relationshipsService.getPersonEvents(personSlug);
    if (events.length > 0) {
      relatedEventsContainer.innerHTML = `<h3>Timeline Events (${events.length})</h3>`;
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      events.slice(0, 6).forEach(event => {
        const card = document.createElement('div');
        card.className = 'entity-card';
        const titleEl = document.createElement('div');
        titleEl.className = 'card-title';
        titleEl.textContent = event.title || '(Untitled)';
        card.appendChild(titleEl);
        const metaEl = document.createElement('div');
        metaEl.className = 'card-meta';
        metaEl.textContent = event.date_start_year ? `${event.date_start_year} CE` : 'Date unknown';
        card.appendChild(metaEl);
        if (event.description_html) {
          const excerptEl = document.createElement('div');
          excerptEl.className = 'card-excerpt';
          excerptEl.innerHTML = event.description_html.substring(0, 150) + '...';
          card.appendChild(excerptEl);
        }
        grid.appendChild(card);
      });
      relatedEventsContainer.appendChild(grid);
      if (events.length > 6) {
        const moreLink = document.createElement('p');
        moreLink.style.color = '#666';
        moreLink.textContent = `... and ${events.length - 6} more events`;
        relatedEventsContainer.appendChild(moreLink);
      }
    } else {
      relatedEventsContainer.innerHTML = '<p style="color: #999;">No related events.</p>';
    }
  }
}

/**
 * Populate relationship sections for a text
 */
function populateTextRelationships(textSlug) {
  if (!window.relationshipsService) return;

  // Related Concepts
  const relatedConceptsContainer = document.getElementById('related-concepts');
  if (relatedConceptsContainer) {
    const concepts = window.relationshipsService.getTextConcepts(textSlug);
    if (concepts.length > 0) {
      relatedConceptsContainer.innerHTML = '<h3>Related Concepts</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      concepts.forEach(concept => {
        grid.appendChild(createEntityCard(concept, 'concept'));
      });
      relatedConceptsContainer.appendChild(grid);
    } else {
      relatedConceptsContainer.innerHTML = '<p style="color: #999;">No related concepts.</p>';
    }
  }

  // Related Persons
  const relatedPersonsContainer = document.getElementById('related-persons');
  if (relatedPersonsContainer) {
    const persons = window.relationshipsService.getTextPersons(textSlug);
    if (persons.length > 0) {
      relatedPersonsContainer.innerHTML = '<h3>Related Persons</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      persons.forEach(person => {
        grid.appendChild(createEntityCard(person, 'person'));
      });
      relatedPersonsContainer.appendChild(grid);
    } else {
      relatedPersonsContainer.innerHTML = '<p style="color: #999;">No related persons.</p>';
    }
  }
}

/**
 * Populate relationship sections for a concept
 */
function populateConceptRelationships(conceptSlug) {
  if (!window.relationshipsService) return;

  // Related Persons
  const relatedPersonsContainer = document.getElementById('related-persons');
  if (relatedPersonsContainer) {
    const persons = window.relationshipsService.getConceptPersons(conceptSlug);
    if (persons.length > 0) {
      relatedPersonsContainer.innerHTML = '<h3>Historical Persons</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      persons.slice(0, 6).forEach(person => {
        grid.appendChild(createEntityCard(person, 'person'));
      });
      relatedPersonsContainer.appendChild(grid);
      if (persons.length > 6) {
        const moreLink = document.createElement('p');
        moreLink.style.color = '#666';
        moreLink.textContent = `... and ${persons.length - 6} more`;
        relatedPersonsContainer.appendChild(moreLink);
      }
    } else {
      relatedPersonsContainer.innerHTML = '<p style="color: #999;">No related persons.</p>';
    }
  }

  // Related Texts
  const relatedTextsContainer = document.getElementById('related-texts');
  if (relatedTextsContainer) {
    const texts = window.relationshipsService.getConceptTexts(conceptSlug);
    if (texts.length > 0) {
      relatedTextsContainer.innerHTML = '<h3>Key Texts</h3>';
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      texts.forEach(text => {
        grid.appendChild(createEntityCard(text, 'text'));
      });
      relatedTextsContainer.appendChild(grid);
    } else {
      relatedTextsContainer.innerHTML = '<p style="color: #999;">No related texts.</p>';
    }
  }

  // Related Events
  const relatedEventsContainer = document.getElementById('related-events');
  if (relatedEventsContainer) {
    const events = window.relationshipsService.getConceptEvents(conceptSlug);
    if (events.length > 0) {
      relatedEventsContainer.innerHTML = `<h3>Timeline Events (${events.length})</h3>`;
      const grid = document.createElement('div');
      grid.className = 'card-grid';
      events.slice(0, 6).forEach(event => {
        const card = document.createElement('div');
        card.className = 'entity-card';
        const titleEl = document.createElement('div');
        titleEl.className = 'card-title';
        titleEl.textContent = event.title || '(Untitled)';
        card.appendChild(titleEl);
        const metaEl = document.createElement('div');
        metaEl.className = 'card-meta';
        metaEl.textContent = event.date_start_year ? `${event.date_start_year} CE` : 'Date unknown';
        card.appendChild(metaEl);
        grid.appendChild(card);
      });
      relatedEventsContainer.appendChild(grid);
      if (events.length > 6) {
        const moreLink = document.createElement('p');
        moreLink.style.color = '#666';
        moreLink.textContent = `... and ${events.length - 6} more events`;
        relatedEventsContainer.appendChild(moreLink);
      }
    } else {
      relatedEventsContainer.innerHTML = '<p style="color: #999;">No related events.</p>';
    }
  }
}

/**
 * Main function to populate relationships based on entity type
 */
function populateEntityRelationships() {
  const context = detectEntityContext();

  if (!context.slug) {
    console.warn('Could not detect entity context');
    return;
  }

  if (context.type === 'person') {
    populatePersonRelationships(context.slug);
  } else if (context.type === 'text') {
    populateTextRelationships(context.slug);
  } else if (context.type === 'concept') {
    populateConceptRelationships(context.slug);
  }
}

// Trigger on page load
document.addEventListener('DOMContentLoaded', populateEntityRelationships);
