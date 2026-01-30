import React from "react";
import { getFilters, setFilter } from "../state/filtersStore";

/**
 * FilterChips
 *
 * Displays active filters as removable chips.
 */
export default function FilterChips() {
  const filters = getFilters();

  const entries = Object.entries(filters).filter(
    ([, value]) => value !== null
  );

  if (entries.length === 0) return null;

  const handleRemove = (key) => {
    setFilter(key, null);
    window.dispatchEvent(new Event("filters-changed"));
  };

  return (
    <div style={{ marginBottom: "16px", display: "flex", gap: "8px", flexWrap: "wrap" }}>
      {entries.map(([key, value]) => (
        <div
          key={key}
          style={{
            background: "#f0f0f0",
            border: "1px solid #ccc",
            borderRadius: "16px",
            padding: "4px 10px",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            fontSize: "14px",
          }}
        >
          <span>
            <b>{labelForKey(key)}:</b> {value}
          </span>
          <button
            onClick={() => handleRemove(key)}
            style={{
              border: "none",
              background: "transparent",
              cursor: "pointer",
              fontWeight: "bold",
            }}
            aria-label={`Remove filter ${key}`}
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}

function labelForKey(key) {
  switch (key) {
    case "country":
      return "Country";
    case "region":
      return "Region";
    case "primary_transport":
      return "Transport";
    case "confidence_band":
      return "Confidence";
    default:
      return key;
  }
}