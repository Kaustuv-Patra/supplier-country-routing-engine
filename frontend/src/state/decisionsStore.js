/**
 * decisionsStore.js
 *
 * Holds in-memory state for routing decisions.
 * Framework-agnostic (no React hooks).
 */

import { fetchDecisions } from "../api/decisionsService";

let state = {
  loading: false,
  error: null,
  meta: null,
  decisions: []
};
console.log("loadDecisions: start");
/**
 * Load decisions from backend.
 */
export async function loadDecisions() {
  state.loading = true;
  state.error = null;

  try {
    const data = await fetchDecisions();
    state.meta = data.meta;
    state.decisions = data.decisions;
    console.log("loadDecisions: success", data.decisions.length);
  } catch (err) {
  // Do NOT overwrite valid data on transient failures
  if (!state.decisions || state.decisions.length === 0) {
    state.error = err.message || "Unknown error";
  }
  console.log("loadDecisions: error", err);
}
 finally {
    state.loading = false;
    console.log("loadDecisions: end");
  }
}

/**
 * Read-only accessor for state.
 */
export function getDecisionsState() {
  return {
    loading: state.loading,
    error: state.error,
    meta: state.meta,
    decisions: state.decisions
  };
}