# NEELGRIVA — System Architecture
add app.py in main folder ( NEELGRIVA/app.py)

## 1. Repository Structure

```text
NEELGRIVA/
├── frontend/                  # React + JavaScript + MapLibre + Tailwind
├── backend/                   # Python + FastAPI
├── database/                  # PostgreSQL + PostGIS schema/migrations
├── ai_models/                 # YOLO11-seg + Scikit-learn models
├── scientific_models/         # OpenDrift + OpenOil
├── geospatial/                # GeoPandas + Shapely + MovingPandas
├── ais/                       # AIS ingestion + pyais + trajectory analysis
├── data_ingestion/            # Sentinel-1, ERA5, Copernicus, Bhoonidhi, AIS
├── shared/                    # Shared schemas, constants and utilities
├── tests/                     # Unit, integration, model and E2E tests
├── scripts/                   # Setup, data, database and development scripts
├── docs/                      # Technical documentation
├── config/                    # Environment/configuration files
├── storage/                   # Raw, processed and generated data
├── docker/                    # Container/deployment files
├── PROJECT_REQUIREMENTS.md
├── ARCHITECTURE.md
├── README.md
├── .env.example
└── .gitignore
```

## 2. Detailed Structure

```text
frontend/
├── public/
└── src/
    ├── assets/
    ├── components/
    │   ├── layout/
    │   ├── map/
    │   ├── investigation/
    │   ├── slick/
    │   ├── vessel/
    │   ├── evidence/
    │   └── timeline/
    ├── pages/
    ├── hooks/
    ├── services/api/
    ├── state/
    ├── utils/
    ├── types/
    ├── App.jsx
    └── main.jsx
├── package.json
├── vite.config.js
└── tailwind.config.js

backend/
├── app/
│   ├── api/routes/
│   │   ├── investigations.py
│   │   ├── slicks.py
│   │   ├── drift.py
│   │   ├── ais.py
│   │   ├── vessels.py
│   │   ├── analysis.py
│   │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── investigation_service.py
│   │   ├── slick_service.py
│   │   ├── drift_service.py
│   │   ├── ais_service.py
│   │   ├── vessel_service.py
│   │   └── ranking_service.py
│   ├── repositories/
│   ├── workers/
│   └── main.py
├── requirements.txt
└── tests/

database/
├── migrations/
├── schema/
│   ├── investigations.sql
│   ├── slicks.sql
│   ├── drift_runs.sql
│   ├── source_regions.sql
│   ├── vessels.sql
│   ├── ais_positions.sql
│   ├── vessel_tracks.sql
│   └── candidate_rankings.sql
├── seeds/
├── functions/
└── README.md

ai_models/
├── oil_slick/
│   ├── model/
│   ├── preprocessing/
│   ├── inference/
│   ├── postprocessing/
│   └── evaluation/
├── vessel_anomaly/
│   ├── features/
│   ├── models/
│   ├── inference/
│   └── evaluation/
├── training/
├── datasets/
├── configs/
└── README.md

scientific_models/
├── opendrift/
│   ├── hindcast/
│   ├── forecast/
│   ├── configuration/
│   └── runners/
├── openoil/
│   ├── hindcast/
│   ├── forecast/
│   ├── configuration/
│   └── runners/
├── environmental/
│   ├── wind.py
│   ├── currents.py
│   └── forcing.py
├── uncertainty/
└── README.md

geospatial/
├── geometry/
│   ├── distances.py
│   ├── intersections.py
│   ├── buffers.py
│   └── transformations.py
├── slick/
├── source_region/
├── trajectories/
├── spatial_filtering/
└── README.md

ais/
├── ingestion/
├── decoding/
│   └── pyais/
├── cleaning/
├── reconstruction/
├── trajectories/
├── behavioural_analysis/
└── metadata/

data_ingestion/
├── sentinel1/
│   ├── download/
│   ├── preprocessing/
│   └── metadata/
├── bhoonidhi/
├── era5/
├── copernicus/
├── copernicus_marine/
├── historical_ais/
└── common/
    ├── validation.py
    ├── provenance.py
    └── formats.py

shared/
├── schemas/
├── constants/
├── enums/
├── geometry/
├── uncertainty/
└── utils/

tests/
├── unit/
├── integration/
│   ├── sar_to_detection/
│   ├── detection_to_drift/
│   ├── drift_to_ais/
│   └── ais_to_ranking/
├── models/
├── api/
├── frontend/
└── e2e/

storage/
├── raw/
│   ├── sar/
│   ├── environmental/
│   └── ais/
├── processed/
├── model_outputs/
├── drift_outputs/
└── exports/
```

## 3. System Layers

```text
┌─────────────────────────────────────────────────────┐
│ FRONTEND                                             │
│ React + JavaScript + Tailwind + MapLibre GL JS      │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP / JSON
                        ▼
┌─────────────────────────────────────────────────────┐
│ BACKEND                                              │
│ Python + FastAPI                                     │
└───────────┬─────────────┬─────────────┬─────────────┘
            │             │             │
            ▼             ▼             ▼
       AI MODELS    SCIENTIFIC      AIS/GIS
       YOLO11-seg   OpenDrift       pyais
       Scikit       OpenOil         MovingPandas
       Learn                        GeoPandas/Shapely
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                    SOURCERANK
                          │
                          ▼
                 PostgreSQL/PostGIS
                          │
                       Redis
```

## 4. Core Data Flow

```text
Sentinel-1 SAR
      ↓
Preprocessing
      ↓
YOLO11-seg
      ↓
Slick detection + geometry
      ↓
ERA5 + Copernicus Marine
      ↓
OpenDrift / OpenOil
      ├── Backward hindcast → probable source region
      └── Forward forecast  → future slick path

Historical AIS
      ↓
pyais
      ↓
AIS cleaning/reconstruction
      ↓
MovingPandas
      ↓
GeoPandas + Shapely
      ↓
Spatial + temporal filtering
      ↓
Behavioural analysis
      ↓
SourceRank
      ↓
Ranked candidate vessels
      ↓
PostgreSQL/PostGIS
      ↓
FastAPI
      ↓
React + MapLibre
```

## 5. Module Responsibilities

| Directory | Responsibility |
|---|---|
| `frontend/` | Investigation console and map UI |
| `backend/` | API, orchestration and application services |
| `database/` | Persistent schema and migrations |
| `ai_models/` | Slick detection and vessel anomaly models |
| `scientific_models/` | Drift and environmental modelling |
| `geospatial/` | Geometry and spatial processing |
| `ais/` | AIS decoding, cleaning and trajectory analysis |
| `data_ingestion/` | External data-source adapters |
| `shared/` | Common data contracts and utilities |
| `tests/` | Automated validation |
| `storage/` | Development data and model outputs |

## 6. Frontend Architecture

The interface should retain the existing NEELGRIVA investigation-console pattern:

```text
┌──────────────┬────────────────────────────┬──────────────┐
│ LEFT PANEL   │            MAP             │ RIGHT PANEL  │
│              │                            │              │
│ State        │ Slick                     │ Source       │
│ Layers       │ Hindcast                  │ Vessels      │
│ Controls     │ Forecast                  │ Evidence     │
│ Legend       │ Vessel                    │              │
│              │ AIS                       │              │
├──────────────┴────────────────────────────┴──────────────┤
│                     TIME TIMELINE                         │
└───────────────────────────────────────────────────────────┘
```

Frontend components:

```text
map/
├── InvestigationMap
├── SlickLayer
├── HindcastLayer
├── ForecastLayer
├── VesselLayer
├── AISLayer
└── SourceRegionLayer

vessel/
├── CandidateList
├── VesselCard
└── VesselTrajectory

evidence/
├── EvidencePanel
├── ScoreBreakdown
└── UncertaintyPanel
```

## 7. Backend Architecture

```text
HTTP Request
     ↓
FastAPI Route
     ↓
Service Layer
     ↓
AI / Scientific / AIS / Geospatial Module
     ↓
Repository / Database
     ↓
Structured JSON Response
```

The frontend must not directly access PostgreSQL, Redis, model files or private data-source credentials.

## 8. AI Model Architecture

### Oil Slick

```text
SAR Image
   ↓
Preprocessing
   ↓
YOLO11-seg
   ↓
Segmentation Mask
   ↓
Postprocessing
   ↓
Slick Geometry + Confidence
```

### Vessel Behaviour

```text
AIS Positions
   ↓
Trajectory Reconstruction
   ↓
Feature Extraction
   ↓
Behaviour Analysis / ML
   ↓
Anomaly Indicators
   ↓
SourceRank
```

## 9. Scientific Model Architecture

```text
ERA5 ───────────────┐
                    ├── Environmental Forcing
Copernicus Marine ──┘
                         ↓
                  OpenDrift/OpenOil
                    ↙          ↘
             Hindcast        Forecast
                ↓                ↓
        Source Region       Future Path
```

## 10. AIS Architecture

```text
Raw AIS
  ↓
pyais
  ↓
Decoded Records
  ↓
Validation / Cleaning
  ↓
Trajectory Reconstruction
  ↓
MovingPandas
  ↓
Movement Features
  ↓
Behaviour Analysis
```

## 11. Geospatial Architecture

```text
Slick Geometry ─────┐
Source Region ──────┼──→ GeoPandas / Shapely
Vessel Track ───────┘
                         ↓
             Distance / Intersection /
             Buffer / Spatial Filtering
```

## 12. SourceRank Architecture

```text
Spatial Evidence ───────┐
Temporal Evidence ──────┤
Drift Compatibility ────┤
Behaviour Evidence ─────┤
Data Confidence ────────┘
             ↓
         SourceRank
             ↓
     Candidate Ranking
             ↓
    Evidence Breakdown
```

SourceRank belongs to the NEELGRIVA application/domain logic. It must not be implemented inside the frontend.

## 13. Database Architecture

PostgreSQL stores persistent application data.

PostGIS handles:
- points
- polygons
- lines
- trajectories
- spatial distance
- intersections
- geographic filtering

Redis handles:
- cache
- temporary state
- job status
- reusable processing results

## 14. Main Database Entities

```text
investigations
      │
      ├── slicks
      │      └── drift_runs
      │             └── source_regions
      │
      ├── candidate_rankings
      │
      └── vessel_tracks
             └── ais_positions

vessels
   └── ais_positions
```

## 15. API Boundary

Minimum API groups:

```text
/investigations
/slicks
/drift
/ais
/vessels
/analysis
/health
```

Example operations:

```text
POST /investigations
GET  /investigations/{id}

POST /slicks/detect

POST /drift/hindcast
POST /drift/forecast

POST /ais/import

GET  /investigations/{id}/vessels

POST /analysis/candidates
POST /analysis/rank

GET /investigations/{id}/source
GET /investigations/{id}/evidence
```

## 16. Shared Data Contracts

Modules should exchange structured objects.

Slick:

```json
{
  "slick_id": "SLK-001",
  "geometry": {},
  "confidence": 0.91,
  "observation_time": "2026-09-01T12:00:00Z",
  "area_km2": 12.4
}
```

Source:

```json
{
  "latitude": 18.42,
  "longitude": 71.63,
  "estimated_time": "2026-09-01T02:00:00Z",
  "uncertainty_km": 6.2,
  "confidence": 0.74
}
```

Candidate:

```json
{
  "mmsi": "636000001",
  "spatial": 0.81,
  "temporal": 0.76,
  "drift": 0.88,
  "behaviour": 0.62,
  "data_confidence": 0.91,
  "source_rank": 0.72
}
```

Values are interface examples, not fixed production values.

## 17. Dependency Rules

```text
Frontend
   ↓
Backend
   ↓
Domain Services
   ↓
AI / Scientific / AIS / Geospatial
   ↓
Database / Data Sources
```

Do not allow direct frontend access to internal databases or model files.

## 18. Uncertainty Flow

```text
SAR Detection
     ↓
Slick Geometry
     ↓
Environmental Data
     ↓
Drift Model
     ↓
Source Region
     ↓
AIS Coverage
     ↓
Candidate Evidence
     ↓
Final Confidence
```

Uncertainty must remain visible throughout the pipeline.

## 19. Investigation States

```text
REGION
  ↓
SLICK
  ↓
VESSEL
```

### REGION
Oil probability and map.

### SLICK
Slick geometry, hindcast, forecast, source region and candidates.

### VESSEL
Selected vessel, trajectory, AIS observations and evidence.

## 20. Error Handling

The system must handle:

- invalid SAR input
- no slick detected
- poor SAR quality
- missing environmental data
- drift-model failure
- missing AIS
- insufficient AIS coverage
- no candidate vessels
- multiple equally plausible candidates
- model failure

Missing evidence should reduce confidence rather than silently becoming a positive attribution signal.

## 21. Security Boundary

The frontend must never contain:
- database credentials
- external API secrets
- private AIS credentials
- model-training credentials

Sensitive data access belongs in the backend/data-ingestion layer.

## 22. Data Provenance

Major results should retain:

- source dataset
- observation/acquisition time
- processing time
- model/version
- relevant parameters
- confidence
- uncertainty

## 23. Development Sequence

```text
1. Repository structure
2. Database schema
3. FastAPI skeleton
4. React investigation console
5. Controlled slick data
6. Controlled drift pipeline
7. Controlled AIS pipeline
8. SourceRank
9. End-to-end integration
10. Real AIS
11. Real environmental data
12. Real SAR ingestion
13. YOLO11-seg integration
14. Validation
15. Deployment
```

## 24. Minimum Working System

The first complete prototype must contain:

```text
frontend/
backend/
database/
ai_models/
scientific_models/
ais/
geospatial/
data_ingestion/
shared/
tests/
```

The prototype must demonstrate:

```text
Slick
 ↓
Detection
 ↓
Drift
 ↓
Probable Source
 ↓
AIS
 ↓
Candidate Filtering
 ↓
SourceRank
 ↓
Explainable Result
```

## 25. Architectural Principle

Each module has one primary responsibility:

```text
React / MapLibre
    → visualization

FastAPI / Python
    → orchestration

YOLO11-seg / Scikit-learn
    → AI/ML

OpenDrift / OpenOil
    → scientific drift modelling

pyais / MovingPandas
    → AIS and trajectory processing

GeoPandas / Shapely
    → geospatial processing

PostgreSQL / PostGIS
    → persistent data and spatial database

Redis
    → cache and temporary processing state

SourceRank
    → NEELGRIVA evidence fusion
```

The system should produce a probable-source ranking with explicit confidence and uncertainty, not a legal declaration of guilt.
