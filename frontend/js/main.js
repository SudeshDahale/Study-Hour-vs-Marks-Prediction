/* ═══════════════════════════════════════════════════
   frontend/js/main.js
   Predictive Analytics Application
   ═══════════════════════════════════════════════════ */

const API_BASE = "https://study-hour-vs-marks-prediction.onrender.com";


let selectedModel = "linear";

// ── On page load ─────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  updateSlider();
  checkAPIAndLoadMetrics();
});

// ── Check API health & load metrics ──────────────────
async function checkAPIAndLoadMetrics() {
  const statusEl = document.getElementById("api-status");

  try {
    // Health check
    const health = await fetch(`${API_BASE}/health`);
    if (!health.ok) throw new Error("API error");

    statusEl.innerHTML = '<span class="dot dot--ok"></span> API Connected ✓';

    // Load metrics
    const res     = await fetch(`${API_BASE}/metrics`);
    const metrics = await res.json();

    // Linear
    document.getElementById("lin-r2").textContent  = metrics.linear.r2;
    document.getElementById("lin-mse").textContent = metrics.linear.mse;
    const linPct = (metrics.linear.r2 * 100).toFixed(1);
    document.getElementById("lin-bar").style.width  = linPct + "%";
    document.getElementById("lin-bar-label").textContent = `R² = ${linPct}% variance explained`;

    // Polynomial
    document.getElementById("poly-r2").textContent  = metrics.polynomial.r2;
    document.getElementById("poly-mse").textContent = metrics.polynomial.mse;
    const polyPct = (metrics.polynomial.r2 * 100).toFixed(1);
    document.getElementById("poly-bar").style.width  = polyPct + "%";
    document.getElementById("poly-bar-label").textContent = `R² = ${polyPct}% variance explained`;

  } catch (err) {
    statusEl.innerHTML =
      '<span class="dot dot--err"></span> API offline — please try again later';
  }
}

// ── Slider ────────────────────────────────────────────
const slider  = document.getElementById("hours-slider");
const display = document.getElementById("hours-display");

slider.addEventListener("input", updateSlider);

function updateSlider() {
  const v   = parseFloat(slider.value);
  display.textContent = v.toFixed(1);

  // Gradient fill on slider track
  const pct = (v / 10) * 100;
  slider.style.background =
    `linear-gradient(90deg, #3b82f6 ${pct}%, #e2e8f0 ${pct}%)`;
}

// ── Model toggle ──────────────────────────────────────
function selectModel(model) {
  selectedModel = model;
  document.getElementById("btn-linear").classList.toggle("active", model === "linear");
  document.getElementById("btn-poly").classList.toggle("active",   model === "polynomial");
}

// ── Predict ───────────────────────────────────────────
async function runPrediction() {
  const hours  = parseFloat(slider.value);
  const btn    = document.getElementById("predict-btn");
  const box    = document.getElementById("result-box");

  btn.textContent = "Predicting…";
  btn.disabled    = true;

  try {
    const res  = await fetch(`${API_BASE}/predict`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ hours, model: selectedModel }),
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    const data = await res.json();
    renderResult(data.predicted_score, hours, selectedModel);

  } catch (err) {
    box.classList.remove("has-result");
    box.innerHTML = `
      <div class="result-placeholder">
        <span class="placeholder-icon">❌</span>
        <p><strong>Error:</strong> ${err.message}<br>
        <small>The API may be temporarily unavailable. Please try again shortly.</small></p>
      </div>`;
  } finally {
    btn.textContent = "🎯 Predict Score";
    btn.disabled    = false;
  }
}

// ── Render result ─────────────────────────────────────
function renderResult(score, hours, model) {
  const box        = document.getElementById("result-box");
  const modelLabel = model === "polynomial" ? "Polynomial (deg=2)" : "Linear";
  const grade      = getGrade(score);

  box.classList.add("has-result");
  box.innerHTML = `
    <div class="result-content">
      <div class="result-score">${score.toFixed(1)}</div>
      <div class="result-unit">/ 100 &nbsp; predicted exam score</div>
      <div class="result-detail">
        <strong>${hours.toFixed(1)} hrs/week</strong> studied &nbsp;·&nbsp;
        Model: <strong>${modelLabel}</strong>
      </div>
      <span class="result-grade"
            style="background:${grade.bg}; color:${grade.fg};">
        ${grade.label}
      </span>
    </div>`;
}

// ── Grade helper ──────────────────────────────────────
function getGrade(score) {
  if (score >= 90) return { label: "🏆  Excellent  (A+)", bg: "#dcfce7", fg: "#166534" };
  if (score >= 80) return { label: "✅  Good       (A)",  bg: "#d1fae5", fg: "#065f46" };
  if (score >= 70) return { label: "👍  Average    (B)",  bg: "#fef9c3", fg: "#713f12" };
  if (score >= 60) return { label: "⚠️  Below Avg  (C)", bg: "#fde68a", fg: "#78350f" };
  return                   { label: "❌  Needs Work (D)", bg: "#fee2e2", fg: "#7f1d1d" };
}

// ── Keyboard shortcut ─────────────────────────────────
document.addEventListener("keydown", e => {
  if (e.key === "Enter") runPrediction();
});
