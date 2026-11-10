# Forest Vision AI (VanaRakshak) 🌲🔥

> **PCCOE International Grand Challenge 2026 (Indradhanu)**  
> **Theme:** AI for Climate Change  
> **Repository:** Working Prototype & GIS Climate Intelligence Platform  

---

## 🌟 The Core Problem We Solved
Most satellite forest dashboards are **passive displays**: they query Sentinel-2 or NASA FIRMS and plot points on a map. When judges look at that, they ask:
> *"What is unique here? You are just grabbing API data and displaying it on a map."*

**Forest Vision AI turns passive observation into active, predictive intelligence across 4 key pillars:**

1. **Predictive Wildfire Spread Simulation (+3h, +6h, +12h):**
   - NASA FIRMS shows where fire was 3–6 hours ago (lagging historical data).
   - Our system couples real-time Open-Meteo wind vectors with Sentinel-2 fuel moisture to simulate **Huygens Elliptical Wavefront propagation**.
   - An interactive time-scrubber lets rangers see the burn perimeter expand downwind in real time.

2. **AI Forest Forensics (Root-Cause Intent Diagnosis):**
   - Standard NDVI only shows green turning brown.
   - Our computer vision geometry classifier evaluates linearity, compactness, and aspect ratio:
     - **Narrow Linear Trails** $\rightarrow$ Illegal Timber Smuggling Roads
     - **Rectangular Parcel Grids** $\rightarrow$ Agricultural Encroachment
     - **Irregular Crater Excavation** $\rightarrow$ Unauthorized Open-Cast Mining

3. **Government Clearance Layer (The "PARIVESH" Engine):**
   - Solves the critical judge question: *"What if this tree felling was legally permitted by the government for highway or dam construction?"*
   - Cross-references canopy loss with official Ministry of Environment, Forest and Climate Change (**MoEFCC PARIVESH**) approved GeoJSON polygons.
   - If legally approved (e.g. NH-66 highway expansion), false emergency sirens are suppressed; if outside, an emergency alert is triggered.

4. **IPCC Carbon Sequestration Loss & AI Reforestation:**
   - Tier-1 Greenhouse Gas formula: $\text{Loss } (tCO_2e) = \text{Area (ha)} \times 150 \times 0.5 \times 3.67$.
   - Generates hyper-local native flora prescription (Teak, Bamboo, Jamun, Ain) for rapid biodiverse restoration.
   - **1-Click Forest Incident Legal Docket:** Produces an official Preliminary Offence Report (POR) under Indian Forest Act 1927 Section 26.

---

## 🚀 Quick Start (Running the Prototype)

### Option A: 1-Click Launch (Windows)
Double-click:
```
start_prototype.bat
```
This automatically starts the server and opens your browser at `http://127.0.0.1:8000`.

### Option B: Command Line (PowerShell)
```powershell
cd C:\Users\Shruti\.gemini\antigravity\scratch\forest-vision-ai
.\.venv\Scripts\python.exe app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 💼 Resume Bullet Points (Copy & Paste for Your Resume)

- **Forest Vision AI (VanaRakshak) — Lead Developer | Hackathon Prototype (Indradhanu 2026)**
  - *Architected a full-stack AI-driven forest intelligence platform integrating Sentinel-2 multispectral imagery and NASA FIRMS active fire telemetry.*
  - *Engineered a predictive wildfire spread simulator implementing the Huygens elliptical wave propagation model coupled with live Open-Meteo meteorological vectors.*
  - *Developed an AI patch forensics classifier using spatial geometry and contour aspect ratio analysis to differentiate illegal timber logging corridors from agricultural encroachment.*
  - *Implemented an automated compliance verification engine cross-referencing deforestation coordinates with Indian MoEFCC PARIVESH infrastructure clearance boundaries.*
  - *Integrated IPCC Tier-1 greenhouse gas estimation models to quantify lost carbon sinks and generate native biodiverse reforestation prescriptions.*
