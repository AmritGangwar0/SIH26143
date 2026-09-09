# NEELGRIVA

**Maritime Oil-Spill Investigation and Source-Attribution System.**

NEELGRIVA detects probable marine oil slicks from SAR imagery, reconstructs a
probable source region using environmental data and drift modelling, correlates
historical AIS data, and ranks candidate vessels using explainable, uncertainty
aware evidence (SourceRank).

> The system answers: *"Which vessel is the most plausible source given the
> available evidence, and how strong is that evidence?"* It does **not** issue a
> legal verdict of guilt.

---

## Repository layout

```
NEELGRIVA/
├── app.py                # root launcher (boots FastAPI)
├── frontend/             # React + JavaScript + MapLibre GL JS + Tailwind
├── backend/              # Python + FastAPI
├── database/             # PostgreSQL + PostGIS schema / migrations
├── ai_models/            # YOLO11-seg + Scikit-learn models
├── scientific_models/    # OpenDrift + OpenOil drift modelling
├── geospatial/           # GeoPandas + Shapely + MovingPandas
├── ais/                  # AIS ingestion + pyais + trajectory analysis
├── data_ingestion/       # Sentinel-1, ERA5, Copernicus, Bhoonidhi, AIS
├── shared/               # shared schemas, constants, utilities
├── tests/                # unit, integration, model, API, e2e tests
├── scripts/              # setup / dev / data scripts
├── docs/                 # technical documentation (source of truth)
├── config/               # environment configuration
└── storage/              # raw, processed, generated data
```

## Quick start

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
# from repo root:
python app.py        # serves API at http://localhost:8000
```

In **demo mode** (`APP_DEMO_MODE=true`) the backend needs no PostgreSQL,
PostGIS, Redis, or external data-source credentials: it runs the full pipeline
(SAR mock → slick detection → environmental forcing → drift → AIS → SourceRank)
on clearly-labelled synthetic/controlled data and persists to a local SQLite
store. Every synthetic result is tagged `data_source: "demo"` so it can never be
mistaken for a live scientific observation.

### Frontend

```bash
cd frontend
npm install
npm run dev          # Vite dev server at http://localhost:5173
# production build:
npm run build
```

The investigation console preserves the dark, three-column investigation
layout from `docs/template.html` (left controls · central map · right evidence,
with a bottom timeline) and replaces the canvas simulation with MapLibre GL JS
rendering real geographic coordinates driven by the backend API.

## Investigation flow

```
REGION → SLICK → VESSEL
```

1. Inspect a region (oil-probability field + base map).
2. Select an oil slick → slick geometry, hindcast, forecast, probable source.
3. Examine ranked candidate vessels → select one → trajectory, AIS, evidence.

## Scientific integrity

- Synthetic/controlled data is **clearly labelled** and isolated from production
  logic (demo mode).
- Probable source is represented as a **region with uncertainty**, never a
  falsely exact point.
- AIS gaps are **not** proof of wrongdoing; behavioural anomalies are
  supporting evidence only.
- SourceRank is explainable: spatial, temporal, drift, behavioural and
  data-confidence components are shown individually.
- Uncertainty remains visible throughout the pipeline.

See `PROJECT_REQUIREMENTS.md`, `ARCHITECTURE.md`, `docs/rules.md` and
`docs/memory.md` for the full specification.
