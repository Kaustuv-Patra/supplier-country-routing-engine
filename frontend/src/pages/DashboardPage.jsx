import { useEffect, useState } from "react";
import { loadDecisions, getDecisionsState } from "../state/decisionsStore";
import { applyFilters, clearFilters } from "../state/filtersStore";

import CountryChart from "../dashboards/CountryChart";
import RegionChart from "../dashboards/RegionChart";
import TransportChart from "../dashboards/TransportChart";
import ConfidenceChart from "../dashboards/ConfidenceChart";
import RoutingCodeChart from "../dashboards/RoutingCodeChart";
import ConfidenceSplitChart from "../dashboards/ConfidenceSplitChart";

import FilterChips from "../components/FilterChips";

import "./DashboardPage.css";

export default function DashboardPage() {
  const [, forceRender] = useState(0);
  const [showRaw, setShowRaw] = useState(false);

  useEffect(() => {
    async function init() {
      await loadDecisions();
      forceRender((x) => x + 1);
    }
    init();

    const handler = () => forceRender((x) => x + 1);
    window.addEventListener("filters-changed", handler);
    return () => window.removeEventListener("filters-changed", handler);
  }, []);

  const state = getDecisionsState();
  const { loading, error, meta, decisions } = state;

  const filteredDecisions = applyFilters(decisions);

  if (loading || !meta) {
    return <div style={{ padding: "16px" }}>Loading decisions...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: "16px", color: "red" }}>
        Error: {error}
      </div>
    );
  }

  const handleClearFilters = () => {
    clearFilters();
    window.dispatchEvent(new Event("filters-changed"));
  };

  return (
    <div style={{ padding: "24px" }}>
      <h2>Routing Decisions Dashboard</h2>

      <p>
        Source: <b>{meta.source}</b> | Count:{" "}
        <b>{filteredDecisions.length}</b>
      </p>

      {/* 🔎 Active filter chips */}
      <FilterChips />

      {/* 🔁 Global reset */}
      <div style={{ marginBottom: "16px" }}>
        <button
          onClick={handleClearFilters}
          style={{ padding: "6px 12px", cursor: "pointer" }}
        >
          Clear Filters
        </button>
      </div>

      <div className="dashboard-grid">
        {/* Row 1 */}
        <div className="chart-card"><CountryChart decisions={filteredDecisions} /></div>
        <div className="chart-card"><RegionChart decisions={filteredDecisions} /></div>
        <div className="chart-card"><TransportChart decisions={filteredDecisions} /></div>

        {/* Row 2 */}
        <div className="chart-card"><ConfidenceChart decisions={filteredDecisions} /></div>
        <div className="chart-card"><RoutingCodeChart decisions={filteredDecisions} /></div>
        <div className="chart-card"><ConfidenceSplitChart decisions={filteredDecisions} /></div>
      </div>

      <div style={{ marginTop: "32px" }}>
        <button onClick={() => setShowRaw(!showRaw)}>
          {showRaw ? "Hide Raw Decisions" : "Show Raw Decisions"}
        </button>

        {showRaw && (
          <pre
            style={{
              maxHeight: "300px",
              overflow: "auto",
              background: "#f5f5f5",
              padding: "12px",
              marginTop: "8px",
            }}
          >
            {JSON.stringify(filteredDecisions, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}