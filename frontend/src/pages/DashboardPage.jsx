/**
 * DashboardPage.jsx
 *
 * Top-level dashboard page.
 * Fetches routing decisions and renders raw output (for now).
 */

import { useEffect, useState } from "react";
import {
  loadDecisions,
  getDecisionsState
} from "../state/decisionsStore";

export default function DashboardPage() {
   console.count("DashboardPage render");
 
  const [, forceRender] = useState(0);

 useEffect(() => {
    async function init() {
      await loadDecisions();
     forceRender((x) => x + 1);
    }
   init();
 }, []);

  const { loading, error, meta, decisions } = getDecisionsState();

  if (loading) {
    return <div>Loading decisions...</div>;
  }

  if (error) {
    return <div style={{ color: "red" }}>Error: {error}</div>;
  }

  return (
    <div style={{ padding: "16px" }}>
      <h2>Routing Decisions Dashboard</h2>

      {meta && (
        <p>
          Source: <b>{meta.source}</b> | Count: <b>{meta.count}</b>
        </p>
      )}

      <pre
        style={{
          background: "#f5f5f5",
          padding: "12px",
          maxHeight: "400px",
          overflow: "auto"
        }}
      >
        {JSON.stringify(decisions, null, 2)}
      </pre>
    </div>
  );
}