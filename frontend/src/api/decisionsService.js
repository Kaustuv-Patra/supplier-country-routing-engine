/**
 * decisionsService.js
 *
 * Responsible ONLY for backend communication.
 * No state management.
 * No UI logic.
 */

const API_BASE_URL = "http://localhost:8000";

/**
 * Fetch all routing decisions.
 * @returns {Promise<{meta: Object, decisions: Array}>}
 */
export async function fetchDecisions() {
  const response = await fetch(`${API_BASE_URL}/decisions`);

  if (!response.ok) {
    const message = `Failed to fetch decisions: ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}