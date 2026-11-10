// Forest Vision AI (VanaRakshak) — Tactical HUD Controller

const maps = {};
let currentView = 'overview';
let thermalModeActive = false;
let scanlinesActive = true;

// Geographic Focus: Koyna Sanctuary Basin (Western Ghats, Maharashtra)
const KOYNA_CENTER = [17.4125, 73.7482];

// High-fidelity polygon contour for detected deforestation footprint
const KOYNA_POLYGON = [
  [17.4220, 73.7280],
  [17.4260, 73.7420],
  [17.4210, 73.7620],
  [17.4120, 73.7740],
  [17.4020, 73.7580],
  [17.3990, 73.7410],
  [17.4080, 73.7290]
];

document.addEventListener('DOMContentLoaded', () => {
  initUtcClock();
  initAllMaps();
  switchView('overview');
});

// Live Mission Clock (UTC)
function initUtcClock() {
  const clockEl = document.getElementById('utcClock');
  function updateTime() {
    const now = new Date();
    const utcStr = now.toISOString().substring(11, 19) + ' UTC';
    if (clockEl) clockEl.textContent = utcStr;
  }
  updateTime();
  setInterval(updateTime, 1000);
}

// Switch Active Tactical View
function switchView(viewName) {
  currentView = viewName;

  // 1. Hide all panels
  document.querySelectorAll('.view-panel').forEach(panel => {
    panel.classList.add('hidden');
  });

  // 2. Clear active nav highlights
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.remove('active-nav');
  });

  // 3. Show selected panel
  const targetPanel = document.getElementById(`view-${viewName}`);
  if (targetPanel) {
    targetPanel.classList.remove('hidden');
  }

  // 4. Highlight active nav
  const targetNav = document.getElementById(`nav-${viewName}`);
  if (targetNav) {
    targetNav.classList.add('active-nav');
  }

  // 5. Invalidate Leaflet canvas to avoid rendering glitches
  setTimeout(() => {
    if (viewName === 'overview' && maps.overview) maps.overview.invalidateSize();
    if (viewName === 'incident-detail' && maps.incident) maps.incident.invalidateSize();
    if (viewName === 'legal-docket' && maps.docket) maps.docket.invalidateSize();
    if (viewName === 'wildfire-simulation' && maps.sim) maps.sim.invalidateSize();
    if (viewName === 'restoration-carbon' && maps.restoration) maps.restoration.invalidateSize();
  }, 120);
}

// Initialize Leaflet Tactical Maps
function initAllMaps() {
  const satTileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';

  // 1. Overview Tactical Map
  if (document.getElementById('overviewMap')) {
    maps.overview = L.map('overviewMap', { zoomControl: false, attributionControl: false }).setView(KOYNA_CENTER, 12);
    L.tileLayer(satTileUrl, { maxZoom: 18 }).addTo(maps.overview);
    L.control.zoom({ position: 'topright' }).addTo(maps.overview);

    // Deforestation Polygon with Neon Pulse
    L.polygon(KOYNA_POLYGON, {
      color: '#ff3366',
      weight: 2.5,
      fillColor: '#ff3366',
      fillOpacity: 0.22,
      dashArray: '4, 4'
    }).addTo(maps.overview);

    // Target Fire Hotspot Marker
    const fireIcon = L.divIcon({
      className: 'custom-div-icon',
      html: '<div class="custom-fire-marker"><i class="fa-solid fa-fire text-xs"></i></div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    L.marker(KOYNA_CENTER, { icon: fireIcon }).addTo(maps.overview);
  }

  // 2. Incident Intel Map
  if (document.getElementById('incidentMap')) {
    maps.incident = L.map('incidentMap', { zoomControl: false, attributionControl: false }).setView(KOYNA_CENTER, 12);
    L.tileLayer(satTileUrl, { maxZoom: 18 }).addTo(maps.incident);
    L.control.zoom({ position: 'topright' }).addTo(maps.incident);

    L.polygon(KOYNA_POLYGON, {
      color: '#ffb703',
      weight: 2.5,
      fillColor: '#ffb703',
      fillOpacity: 0.25
    }).addTo(maps.incident);

    const fireIcon = L.divIcon({
      className: 'custom-div-icon',
      html: '<div class="custom-fire-marker" style="background: radial-gradient(circle, #ffb703 30%, #b37400 90%);"><i class="fa-solid fa-crosshairs text-xs"></i></div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    L.marker(KOYNA_CENTER, { icon: fireIcon }).addTo(maps.incident);
  }

  // 3. Legal Dossier Mini Map
  if (document.getElementById('docketMiniMap')) {
    maps.docket = L.map('docketMiniMap', { zoomControl: false, attributionControl: false }).setView(KOYNA_CENTER, 12);
    L.tileLayer(satTileUrl, { maxZoom: 18 }).addTo(maps.docket);

    L.polygon(KOYNA_POLYGON, {
      color: '#00d2ff',
      weight: 2,
      fillColor: '#00d2ff',
      fillOpacity: 0.25
    }).addTo(maps.docket);

    const markerIcon = L.divIcon({
      className: 'custom-div-icon',
      html: '<div class="custom-fire-marker" style="width:24px;height:24px;"><i class="fa-solid fa-location-pin text-[10px]"></i></div>',
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });
    L.marker(KOYNA_CENTER, { icon: markerIcon }).addTo(maps.docket);
  }

  // 4. Wildfire Physics Map
  if (document.getElementById('simMap')) {
    maps.sim = L.map('simMap', { zoomControl: false, attributionControl: false }).setView(KOYNA_CENTER, 12);
    L.tileLayer(satTileUrl, { maxZoom: 18 }).addTo(maps.sim);
    L.control.zoom({ position: 'topright' }).addTo(maps.sim);

    const fireIcon = L.divIcon({
      className: 'custom-div-icon',
      html: '<div class="custom-fire-marker"><i class="fa-solid fa-fire text-xs"></i></div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    L.marker(KOYNA_CENTER, { icon: fireIcon }).addTo(maps.sim);

    renderSimulationEnvelope(3.0);
  }

  // 5. Bio-Restoration Map
  if (document.getElementById('restorationMap')) {
    maps.restoration = L.map('restorationMap', { zoomControl: false, attributionControl: false }).setView(KOYNA_CENTER, 12);
    L.tileLayer(satTileUrl, { maxZoom: 18 }).addTo(maps.restoration);
    L.control.zoom({ position: 'topright' }).addTo(maps.restoration);

    L.polygon(KOYNA_POLYGON, {
      color: '#00f5a0',
      weight: 2.5,
      dashArray: '6, 6',
      fillColor: '#00f5a0',
      fillOpacity: 0.18
    }).addTo(maps.restoration);

    const plantIcon = L.divIcon({
      className: 'custom-div-icon',
      html: '<div class="custom-plant-marker"><i class="fa-solid fa-seedling text-xs"></i></div>',
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });
    L.marker(KOYNA_CENTER, { icon: plantIcon }).addTo(maps.restoration);
  }
}

// Wildfire Huygens Ellipse Generation
let simPolygonLayer = null;
let simDashedOuterLayer = null;

function renderSimulationEnvelope(hours) {
  if (!maps.sim) return;

  if (simPolygonLayer) maps.sim.removeLayer(simPolygonLayer);
  if (simDashedOuterLayer) maps.sim.removeLayer(simDashedOuterLayer);

  const factor = Math.max(hours / 3.0, 0.2);

  // Elliptical coordinates propagating eastward (azimuth 87°)
  const basePolygon = [
    [17.4125 + 0.015 * factor, 73.7482 - 0.010 * factor],
    [17.4125 + 0.025 * factor, 73.7482 + 0.025 * factor],
    [17.4125 + 0.010 * factor, 73.7482 + 0.055 * factor],
    [17.4125 - 0.015 * factor, 73.7482 + 0.035 * factor],
    [17.4125 - 0.020 * factor, 73.7482 - 0.005 * factor]
  ];

  const outerEnvelope = [
    [17.4125 + 0.022 * factor, 73.7482 - 0.018 * factor],
    [17.4125 + 0.035 * factor, 73.7482 + 0.035 * factor],
    [17.4125 + 0.018 * factor, 73.7482 + 0.075 * factor],
    [17.4125 - 0.022 * factor, 73.7482 + 0.045 * factor],
    [17.4125 - 0.028 * factor, 73.7482 - 0.012 * factor]
  ];

  if (hours > 0) {
    simPolygonLayer = L.polygon(basePolygon, {
      color: '#ff3366',
      weight: 2,
      fillColor: '#ff3366',
      fillOpacity: 0.28
    }).addTo(maps.sim);

    simDashedOuterLayer = L.polygon(outerEnvelope, {
      color: '#ffb703',
      weight: 1.5,
      dashArray: '6, 6',
      fill: false
    }).addTo(maps.sim);
  }
}

// Wildfire Slider Interaction
function onWfSliderChange(val) {
  const hours = parseFloat(val);
  document.getElementById('wfSliderBadge').textContent = `+${hours.toFixed(1)} HOURS FORECAST`;
  document.getElementById('wfSimHorizonText').textContent = `+${hours.toFixed(1)} HOURS`;

  let area = 0.5;
  let reach = 0.05;

  if (hours <= 0) {
    area = 0.5;
    reach = 0.05;
  } else if (hours <= 3) {
    area = (hours / 3.0) * 188.8;
    reach = (hours / 3.0) * 1.83;
  } else if (hours <= 6) {
    area = 188.8 + ((hours - 3) / 3.0) * 187.7;
    reach = 1.83 + ((hours - 3) / 3.0) * 1.82;
  } else {
    area = 376.5 + ((hours - 6) / 6.0) * 405.5;
    reach = 3.65 + ((hours - 6) / 6.0) * 3.75;
  }

  document.getElementById('wfSimAreaText').textContent = `${area.toFixed(1)} HA`;
  document.getElementById('wfSimReachText').textContent = `${reach.toFixed(2)} KM`;
  document.getElementById('simCardTitle').textContent = `PROJECTED BURN ENVELOPE: +${hours.toFixed(1)} HOURS`;
  document.getElementById('simCardDesc').textContent = `Projected Area: ${area.toFixed(1)} ha \u2022 Forward Reach: ${reach.toFixed(2)} km`;

  renderSimulationEnvelope(hours);
}

function setWfSlider(h) {
  const slider = document.getElementById('wfTimeSlider');
  if (slider) {
    slider.value = h;
    onWfSliderChange(h);
  }
}

function resetSimInputs() {
  setWfSlider(3);
}

function runSimAnimation() {
  let step = 0;
  const timer = setInterval(() => {
    step += 1;
    if (step > 12) {
      clearInterval(timer);
    } else {
      setWfSlider(step);
    }
  }, 220);
}

// Authentication Checklist Score Calculator
function updateAuthScore() {
  const checkboxes = document.querySelectorAll('.auth-check');
  let checkedCount = 0;
  checkboxes.forEach(cb => { if (cb.checked) checkedCount++; });

  const pct = Math.round((checkedCount / checkboxes.length) * 100);
  const badge = document.getElementById('authScoreBadge');
  if (badge) {
    badge.textContent = `${checkedCount} OF ${checkboxes.length} VERIFIED (${pct}%)`;
    if (pct === 100) {
      badge.className = 'text-[#00f5a0] font-bold text-shadow-[0_0_10px_#00f5a0]';
    } else {
      badge.className = 'text-[#00f5a0] font-bold';
    }
  }
}

// HUD Controls Toggles
function toggleThermalMode() {
  thermalModeActive = !thermalModeActive;
  const btn = document.getElementById('btnThermalToggle');
  if (thermalModeActive) {
    document.body.style.filter = 'hue-rotate(290deg) contrast(1.15)';
    btn.className = 'px-2.5 py-1 rounded text-black bg-amber-400 font-bold transition flex items-center gap-1.5 shadow-[0_0_10px_rgba(255,183,3,0.5)]';
  } else {
    document.body.style.filter = 'none';
    btn.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition flex items-center gap-1.5';
  }
}

function toggleScanlines() {
  scanlinesActive = !scanlinesActive;
  const scanEl = document.querySelector('.hud-scanlines');
  const btn = document.getElementById('btnScanlineToggle');
  if (scanlinesActive) {
    scanEl.style.display = 'block';
    btn.className = 'px-2.5 py-1 rounded text-[#00f5a0] bg-[#00f5a0]/15 font-semibold transition flex items-center gap-1';
  } else {
    scanEl.style.display = 'none';
    btn.className = 'px-2.5 py-1 rounded text-slate-400 hover:text-white transition flex items-center gap-1';
  }
}

// Tactical Modals & Actions
function exportTacticalReport() {
  window.print();
}

function exportSnapshotModal() {
  alert("[TACTICAL HUD] Exporting Raw GeoJSON Feature Collection + Sentinel-2 Tile T43QDB bands.");
}

function exportAnalysisModal() {
  alert("[TACTICAL HUD] Exporting Computer Vision Geometry Contour Report (.JSON formatted).");
}

function generateCourtDocketPDF() {
  window.print();
}

function editAssumptionsModal() {
  alert("[IPCC MODEL PARAMETERS]\n• Biomass Density: 150 t/ha (Tropical Deciduous)\n• Carbon Fraction: 0.50\n• CO2e Ratio: 44/12 (3.67x)\n• Sapling Density: 1,100 stems/ha");
}

function exportDraftPlanModal() {
  alert("[REFORESTATION PRESCRIPTION]\n• Target: 16,280 Indigenous Western Ghats Saplings\n• Species: Tectona grandis (Teak) + Dendrocalamus strictus (Bamboo)\n• Timeline: ~5.7 Years to Equilibrium");
}

function addReviewNotePrompt() {
  const note = prompt("Enter Forest Range Officer Field Observation:");
  if (note) {
    alert("Record appended to chain of custody audit trail:\n'" + note + "'");
  }
}
