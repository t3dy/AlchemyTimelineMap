/**
 * ALCHEMYTIMELINEMAP Timeline Viewer
 * Renders 582 timeline events grouped by era as index cards linking to full event pages.
 */

(function () {
  "use strict";

  const ERA_ORDER = ["LATE_ANTIQUE", "MEDIEVAL", "EARLY_MODERN"];
  const ERA_LABELS = {
    LATE_ANTIQUE: "Late Antiquity (3rd–7th centuries)",
    MEDIEVAL: "Medieval (7th–15th centuries)",
    EARLY_MODERN: "Early Modern (15th–18th centuries)",
  };

  let allEvents = [];
  let conceptsIndex = {};  // slug → label
  let personsIndex = {};   // slug → name
  let activeEras = new Set();
  let activePersonSlugs = new Set();
  let activeConceptSlugs = new Set();

  // ── Helpers ──────────────────────────────────────────────────────────────────

  function escHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function truncate(str, maxLen) {
    if (!str) return "";
    const s = str.replace(/\s+/g, " ").trim();
    return s.length <= maxLen ? s : s.slice(0, maxLen - 1).trimEnd() + "…";
  }

  function eraFromYear(year) {
    if (year == null) return "MEDIEVAL";
    const y = parseInt(year, 10);
    if (y < 600) return "LATE_ANTIQUE";
    if (y < 1400) return "MEDIEVAL";
    return "EARLY_MODERN";
  }

  // ── Rendering ─────────────────────────────────────────────────────────────────

  function buildEventCard(event) {
    const era = event.era || eraFromYear(event.date_start_year);
    const locationDisplay = event.place_name
      ? event.place_name
      : (event.location_slug || "").replace(/-/g, " ");

    // Entity chips: persons + concepts (slug → label)
    const personChips = (event.persons_involved || []).map((slug) => {
      const name = personsIndex[slug] || slug;
      return `<a href="persons/${escHtml(slug)}.html" class="chip chip--person">${escHtml(name)}</a>`;
    }).join("");

    const conceptChips = (event.concepts_involved || []).map((slug) => {
      const label = conceptsIndex[slug] || slug.replace(/-/g, " ");
      return `<a href="concepts/${escHtml(slug)}.html" class="chip chip--concept">${escHtml(label)}</a>`;
    }).join("");

    const textChips = (event.texts_involved || []).length > 0
      ? (event.texts_involved || []).map((slug) => {
          return `<a href="texts/${escHtml(slug)}.html" class="chip chip--text">${escHtml(slug.replace(/-/g, " "))}</a>`;
        }).join("")
      : "";

    const chipsRow = personChips + textChips + conceptChips;

    const summary = truncate(event.summary || event.description || "", 220);

    return `
      <article class="timeline-card" data-era="${escHtml(era)}"
        data-persons="${escHtml((event.persons_involved || []).join(","))}"
        data-concepts="${escHtml((event.concepts_involved || []).join(","))}">
        <div class="timeline-card__meta">
          <span class="timeline-card__date">${escHtml(event.date_label || "Undated")}</span>
          <span class="timeline-card__location">${escHtml(locationDisplay)}</span>
        </div>
        ${summary ? `<p class="timeline-card__summary">${escHtml(summary)}</p>` : ""}
        ${chipsRow ? `<div class="timeline-card__chips">${chipsRow}</div>` : ""}
        <a href="events/${escHtml(event.slug)}.html" class="timeline-card__link">Read full entry →</a>
      </article>`;
  }

  function renderTimeline(events) {
    const container = document.getElementById("timeline-container");
    if (!container) return;

    // Group by era
    const byEra = { LATE_ANTIQUE: [], MEDIEVAL: [], EARLY_MODERN: [] };
    events.forEach((e) => {
      const era = e.era || eraFromYear(e.date_start_year);
      if (byEra[era]) byEra[era].push(e);
    });

    // Sort within each era by year
    ERA_ORDER.forEach((era) => {
      byEra[era].sort((a, b) => {
        const ay = parseInt(a.date_start_year, 10) || 0;
        const by_ = parseInt(b.date_start_year, 10) || 0;
        return ay - by_;
      });
    });

    container.innerHTML = ERA_ORDER.map((era) => {
      const elist = byEra[era];
      if (elist.length === 0) return "";
      return `
        <section class="era-section" id="era-${era}">
          <h3 class="era-section__title">${escHtml(ERA_LABELS[era])}</h3>
          <p class="era-section__count">${elist.length} event${elist.length !== 1 ? "s" : ""}</p>
          <div class="era-section__grid">
            ${elist.map(buildEventCard).join("")}
          </div>
        </section>`;
    }).join("");

    updateCount(events.length);
  }

  // ── Filtering ─────────────────────────────────────────────────────────────────

  function matchesFilters(event) {
    const era = event.era || eraFromYear(event.date_start_year);

    if (activeEras.size > 0 && !activeEras.has(era)) return false;

    if (activePersonSlugs.size > 0) {
      const ep = event.persons_involved || [];
      if (!ep.some((s) => activePersonSlugs.has(s))) return false;
    }

    if (activeConceptSlugs.size > 0) {
      const ec = event.concepts_involved || [];
      if (!ec.some((s) => activeConceptSlugs.has(s))) return false;
    }

    return true;
  }

  function applyFilters() {
    const filtered = allEvents.filter(matchesFilters);
    renderTimeline(filtered);
  }

  // ── Filter UI ─────────────────────────────────────────────────────────────────

  function updateCount(n) {
    const el = document.getElementById("timeline-event-count");
    if (el) {
      const total = allEvents.length;
      el.textContent = n === total
        ? `Showing all ${total} events`
        : `Showing ${n} of ${total} events`;
    }
  }

  function buildEraFilterUI() {
    const container = document.querySelector(".era-filter-options");
    if (!container) return;
    container.innerHTML = ERA_ORDER.map((era) => {
      const count = allEvents.filter((e) => (e.era || eraFromYear(e.date_start_year)) === era).length;
      return `<label class="filter-chip">
        <input type="checkbox" value="${escHtml(era)}" data-filter="era">
        ${escHtml(ERA_LABELS[era])} <em>(${count})</em>
      </label>`;
    }).join("");
  }

  function buildPersonFilterUI() {
    const container = document.querySelector(".person-filter-options");
    if (!container) return;

    // Tally persons across all events
    const counts = {};
    allEvents.forEach((e) => {
      (e.persons_involved || []).forEach((slug) => {
        counts[slug] = (counts[slug] || 0) + 1;
      });
    });

    const sorted = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 80); // top 80 most-referenced persons

    container.innerHTML = sorted.map(([slug, count]) => {
      const name = personsIndex[slug] || slug.replace(/-/g, " ");
      return `<label class="filter-chip">
        <input type="checkbox" value="${escHtml(slug)}" data-filter="person">
        ${escHtml(name)} <em>(${count})</em>
      </label>`;
    }).join("");
  }

  function buildConceptFilterUI() {
    const container = document.querySelector(".concept-filter-options");
    if (!container) return;

    const counts = {};
    allEvents.forEach((e) => {
      (e.concepts_involved || []).forEach((slug) => {
        counts[slug] = (counts[slug] || 0) + 1;
      });
    });

    const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);

    container.innerHTML = sorted.map(([slug, count]) => {
      const label = conceptsIndex[slug] || slug.replace(/-/g, " ");
      return `<label class="filter-chip">
        <input type="checkbox" value="${escHtml(slug)}" data-filter="concept">
        ${escHtml(label)} <em>(${count})</em>
      </label>`;
    }).join("");
  }

  function attachFilterListeners() {
    document.addEventListener("change", (e) => {
      const input = e.target;
      if (input.tagName !== "INPUT" || input.type !== "checkbox") return;

      const kind = input.getAttribute("data-filter");
      const val = input.value;

      if (kind === "era") {
        input.checked ? activeEras.add(val) : activeEras.delete(val);
      } else if (kind === "person") {
        input.checked ? activePersonSlugs.add(val) : activePersonSlugs.delete(val);
      } else if (kind === "concept") {
        input.checked ? activeConceptSlugs.add(val) : activeConceptSlugs.delete(val);
      }

      applyFilters();
    });

    const clearBtn = document.getElementById("clear-filters-btn");
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        activeEras.clear();
        activePersonSlugs.clear();
        activeConceptSlugs.clear();
        document.querySelectorAll("[data-filter]").forEach((cb) => (cb.checked = false));
        const searches = document.querySelectorAll(".filter-search");
        searches.forEach((s) => (s.value = ""));
        document.querySelectorAll(".filter-chip").forEach((chip) => (chip.style.display = ""));
        applyFilters();
      });
    }

    // Live search within filter lists
    document.querySelectorAll(".filter-search").forEach((input) => {
      input.addEventListener("input", () => {
        const q = input.value.toLowerCase();
        const target = input.getAttribute("data-search-target");
        document.querySelectorAll(`.${target} .filter-chip`).forEach((chip) => {
          chip.style.display = chip.textContent.toLowerCase().includes(q) ? "" : "none";
        });
      });
    });
  }

  // ── Init ─────────────────────────────────────────────────────────────────────

  async function init() {
    try {
      const resp = await fetch("data/data.json");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      allEvents = data.events || [];

      // Build lookup indexes from persons/concepts arrays
      (data.persons || []).forEach((p) => { personsIndex[p.slug] = p.name; });
      (data.concepts || []).forEach((c) => { conceptsIndex[c.slug] = c.label; });

      // Ensure all events have era derived
      allEvents.forEach((e) => {
        if (!e.era) e.era = eraFromYear(e.date_start_year);
      });

      buildEraFilterUI();
      buildPersonFilterUI();
      buildConceptFilterUI();
      attachFilterListeners();
      renderTimeline(allEvents);

    } catch (err) {
      console.error("Timeline load error:", err);
      const container = document.getElementById("timeline-container");
      if (container) {
        container.innerHTML = `<p class="error-message">Error loading timeline data: ${escHtml(err.message)}</p>`;
      }
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
