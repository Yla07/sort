const $ = (selector) => document.querySelector(selector);
const state = { data: [], isSorted: false };

async function request(url, options = {}) {
  const response = await fetch(url, { headers: { "Content-Type": "application/json" }, ...options });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "The Python backend rejected the request.");
  return payload;
}

function render() {
  const bars = $("#bars");
  $("#graph-label").textContent = state.isSorted ? "Sorted output" : "Input order";
  $("#count-label").textContent = `${state.data.length} ${state.data.length === 1 ? "value" : "values"}`;
  if (!state.data.length) {
    bars.innerHTML = '<div class="empty-state">Generate or add values<br><span>Your dataset will appear here.</span></div>';
    $("#summary").textContent = "Waiting for data";
    return;
  }
  const min = Math.min(...state.data);
  const max = Math.max(...state.data);
  const range = max - min || 1;
  $("#summary").textContent = `Range ${min} — ${max}`;
  bars.innerHTML = state.data.map((value, index) => {
    const height = Math.max(5, ((value - min) / range) * 88 + 5);
    return `<div class="bar-wrap" style="--height: ${height}%"><span class="bar-value">${value}</span><div class="bar" style="height: ${height}%; animation-delay: ${index * 18}ms"></div></div>`;
  }).join("");
}

function setData(payload, message, isSorted = false) {
  state.data = payload.data;
  state.isSorted = isSorted;
  render();
  $("#message").textContent = message;
}

async function generate() {
  const minimum = Number($("#min-input").value);
  const maximum = Number($("#max-input").value);
  const size = Number($("#size-input").value);
  if (maximum < minimum || size < 1 || size > 1000) throw new Error("Check the range and choose 1–1000 values.");
  setData(await request("/api/generate", { method: "POST", body: JSON.stringify({ min: minimum, max: maximum, size }) }), `Generated ${size} random values.`);
}

async function addValue() {
  const value = Number($("#value-input").value);
  if (!Number.isInteger(value)) throw new Error("Enter a whole number first.");
  const data = [...state.data, value];
  setData(await request("/api/data", { method: "POST", body: JSON.stringify({ data }) }), `Added ${value} to the dataset.`);
  $("#value-input").value = "";
}

async function sort() {
  const algorithm = $("#algorithm-select").value;
  const count = state.data.length;
  setData(await request("/api/sort", { method: "POST", body: JSON.stringify({ algorithm }) }), `Sorted ${count} values with ${$("#algorithm-select").selectedOptions[0].text}.`, true);
}

function reportError(error) { $("#message").textContent = error.message; }
$("#generate-button").addEventListener("click", () => generate().catch(reportError));
$("#add-button").addEventListener("click", () => addValue().catch(reportError));
$("#sort-button").addEventListener("click", () => sort().catch(reportError));
$("#clear-button").addEventListener("click", () => request("/api/data", { method: "DELETE" }).then((payload) => setData(payload, "Dataset cleared.")).catch(reportError));
request("/api/health").then(() => { $("#status-dot").classList.add("online"); $("#connection-status").textContent = "Python backend online"; return request("/api/data"); }).then((payload) => setData(payload, "Ready when you are.")).catch(() => { $("#connection-status").textContent = "Backend unavailable"; $("#message").textContent = "Start server.py to connect this workspace."; });