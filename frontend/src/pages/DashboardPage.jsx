import { useEffect, useState } from "react";
import { loadDecisions, getDecisionsState } from "../state/decisionsStore";

import CountryChart from "../dashboards/CountryChart";
import RegionChart from "../dashboards/RegionChart";
import TransportChart from "../dashboards/TransportChart";
import ConfidenceChart from "../dashboards/ConfidenceChart";
import RoutingCodeChart from "../dashboards/RoutingCodeChart";
import ConfidenceSplitChart from "../dashboards/ConfidenceSplitChart";

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
  }, []);

  const { loading, error, meta, decisions } = getDecisionsState();

  if (loading) return <div style={{ padding: "16px" }}>Loading...</div>;
  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;

  return (
    <div style={{ padding: "24px" }}>
      <h2>Routing Decisions Dashboard</h2>

      <p>
        Source: <b>{meta.source}</b> | Count: <b>{meta.count}</b>
      </p>

      <div className="dashboard-grid">
        {/* Row 1 */}
        <div className="chart-card"><CountryChart decisions={decisions} /></div>
        <div className="chart-card"><RegionChart decisions={decisions} /></div>
        <div className="chart-card"><TransportChart decisions={decisions} /></div>

        {/* Row 2 */}
        <div className="chart-card"><ConfidenceChart decisions={decisions} /></div>
        <div className="chart-card"><RoutingCodeChart decisions={decisions} /></div>
        <div className="chart-card"><ConfidenceSplitChart decisions={decisions} /></div>
      </div>

      <div style={{ marginTop: "32px" }}>
        <button onClick={() => setShowRaw(!showRaw)}>
          {showRaw ? "Hide Raw Decisions" : "Show Raw Decisions"}
        </button>

        {showRaw && (
          <pre style={{ maxHeight: "300px", overflow: "auto" }}>
            {JSON.stringify(decisions, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}