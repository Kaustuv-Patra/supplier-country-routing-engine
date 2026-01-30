/**
 * filtersStore
 *
 * Centralized filter state for cross-filtering dashboard.
 * This store is intentionally simple and synchronous.
 *
 * Filters supported:
 * - country
 * - region
 * - primary_transport
 * - confidence_band
 */

let filters = {
  country: null,
  region: null,
  primary_transport: null,
  confidence_band: null, // "low" | "medium" | "high"
};

/**
 * Update a single filter.
 */
export function setFilter(key, value) {
  if (!(key in filters)) {
    throw new Error(`Unknown filter key: ${key}`);
  }
  filters[key] = value;
}

/**
 * Clear all filters.
 */
export function clearFilters() {
  filters = {
    country: null,
    region: null,
    primary_transport: null,
    confidence_band: null,
  };
}

/**
 * Get current filter state (read-only).
 */
export function getFilters() {
  return { ...filters };
}

/**
 * Apply filters to decisions list.
 */
export function applyFilters(decisions) {
  if (!decisions || decisions.length === 0) return decisions;

  return decisions.filter((d) => {
    if (filters.country && d.predicted_country !== filters.country) {
      return false;
    }

    if (filters.region && d.region !== filters.region) {
      return false;
    }

    if (
      filters.primary_transport &&
      d.primary_transport !== filters.primary_transport
    ) {
      return false;
    }

    if (filters.confidence_band) {
      const c = d.confidence ?? 0;

      if (filters.confidence_band === "low" && c >= 0.08) return false;
      if (
        filters.confidence_band === "medium" &&
        (c < 0.08 || c > 0.1)
      )
        return false;
      if (filters.confidence_band === "high" && c <= 0.1) return false;
    }

    return true;
  });
}