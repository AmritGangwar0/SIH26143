# NEELGRIVA — Project Requirements

## 1. Project

**Name:** NEELGRIVA  
**Type:** Maritime Oil-Spill Investigation and Source Attribution System  
**Purpose:** Detect probable marine oil slicks from SAR imagery, reconstruct probable source regions using environmental data and drift modelling, correlate historical AIS data, and rank candidate vessels using explainable evidence.

The system must provide **probable attribution with confidence and uncertainty**, not a legal declaration of responsibility.

---

## 2. Required Technology Stack

### Frontend
- React.js
- JavaScript
- MapLibre GL JS
- Tailwind CSS

### Backend
- Python
- FastAPI

### Database
- PostgreSQL
- PostGIS
- Redis

### AI / ML
- YOLO11-seg
- Scikit-learn

### Scientific Modelling
- OpenDrift
- OpenOil

### Data Sources / Interfaces
- Sentinel-1 SAR
- ERA5
- Copernicus Marine
- Copernicus datasets where applicable
- Bhoonidhi where applicable
- Historical AIS

### Geospatial / AIS Processing
- GeoPandas
- Shapely
- MovingPandas
- pyais

---

# 3. Core System Workflow

```text
Sentinel-1 SAR
      ↓
Image preprocessing
      ↓
YOLO11-seg
      ↓
Potential oil slick + segmentation
      ↓
Slick geometry / characteristics
      ↓
ERA5 + Copernicus Marine
      ↓
OpenDrift / OpenOil
      ↓
Backward hindcast ─────→ Probable source region
      ↓
Forward forecast ──────→ Future slick path
      ↓
Historical AIS
      ↓
pyais
      ↓
MovingPandas
      ↓
GeoPandas + Shapely
      ↓
Spatiotemporal candidate filtering
      ↓
Vessel behavioural analysis
      ↓
Scikit-learn / statistical analysis
      ↓
SourceRank evidence fusion
      ↓
Ranked candidate vessels
      ↓
FastAPI
      ↓
React + MapLibre GL JS
      ↓
Investigation Console
```

---

# 4. Functional Requirements

## FR-01 Investigation Creation

The system shall allow the user to create or open an oil-spill investigation.

Each investigation shall contain:
- Investigation ID
- Date/time
- Geographic area
- Input SAR scene
- Detection results
- Drift runs
- Source estimate
- Candidate vessels
- Evidence scores
- Confidence/uncertainty information

---

## FR-02 SAR Image Input

The system shall accept Sentinel-1 SAR imagery or a supported preprocessed SAR image.

Required processing:
1. Load image
2. Validate image
3. Preprocess image
4. Run oil-slick detection
5. Generate segmentation mask
6. Convert detection to geospatial geometry
7. Store detection result

---

## FR-03 Oil-Slick Detection

YOLO11-seg shall be used for the prototype oil-slick detection module.

Output:
- Detection mask
- Bounding region where applicable
- Confidence
- Slick geometry
- Detection timestamp
- Source image reference

The system shall not treat every dark SAR region as an oil spill.

---

## FR-04 Slick Characterisation

The system shall calculate or store:
- Slick area
- Approximate length/width
- Geometry
- Detection confidence
- Observation time
- Geographic coordinates

Environmental context should be attached where available.

---

## FR-05 Environmental Data

The system shall obtain or accept:
- Wind information from ERA5 or equivalent supported data
- Ocean current information from Copernicus Marine or equivalent supported data
- Relevant environmental timestamps and spatial coverage

Environmental data shall be associated with the investigation time and area.

---

## FR-06 Drift Modelling

OpenDrift/OpenOil shall provide the drift-modelling layer.

The system shall support:

### Backward Hindcast
Estimate:
- probable source region
- probable source time
- trajectory uncertainty

### Forward Forecast
Estimate:
- future slick trajectory
- probable future position
- trajectory uncertainty

The output shall be represented as a probability/uncertainty region rather than a falsely exact path.

---

## FR-07 Historical AIS Input

The system shall accept historical AIS data containing, where available:
- MMSI
- Timestamp
- Latitude
- Longitude
- Speed
- Course
- Heading where available
- Vessel metadata where available

Raw AIS messages shall be decodable using pyais.

---

## FR-08 Vessel Trajectory Reconstruction

The system shall reconstruct vessel trajectories from AIS observations.

MovingPandas shall be used where appropriate for:
- trajectory construction
- movement analysis
- temporal trajectory operations

The system shall preserve the original AIS observations.

---

## FR-09 Candidate Vessel Filtering

Candidate vessels shall be filtered using:
- probable source region
- probable source time
- spatial proximity
- temporal compatibility
- trajectory compatibility

GeoPandas and Shapely shall support geospatial operations.

---

## FR-10 Vessel Behaviour Analysis

The system shall calculate supporting behavioural indicators where sufficient AIS data exists.

Possible indicators:
- abnormal speed
- unusual course changes
- stopping/loitering
- route deviation
- unusual movement pattern
- AIS gaps

Behavioural anomalies shall be treated as **supporting evidence only**.

An AIS gap shall never automatically mean that a vessel caused the spill.

---

# 5. SourceRank Requirements

SourceRank shall combine multiple evidence categories.

Minimum categories:

1. Spatial evidence
2. Temporal evidence
3. Drift compatibility
4. Behavioural evidence
5. Data confidence

Example conceptual score:

```text
SourceRank =
    spatial contribution
  + temporal contribution
  + drift contribution
  + behavioural contribution
  + data-confidence contribution
```

The exact weighting shall remain configurable.

The system shall show the individual evidence components so that the final ranking is explainable.

The score shall not automatically be described as a calibrated probability.

---

# 6. Uncertainty Requirements

The system shall explicitly represent uncertainty in:
- SAR detection
- Slick geometry
- Environmental data
- Drift modelling
- AIS availability
- Source location
- Candidate ranking

The UI shall distinguish:
- observation
- model estimate
- probability
- uncertainty
- supporting evidence

The system shall not claim legal responsibility.

Preferred terminology:
- Probable source
- Candidate vessel
- Most plausible candidate
- Evidence score
- Confidence
- Uncertainty
- Supporting evidence

Avoid:
- Confirmed culprit
- Guaranteed source
- Proven responsible vessel
- Exact source
- 100% attribution

---

# 7. Database Requirements

## PostgreSQL + PostGIS

Required logical entities:

### investigations
- id
- name
- status
- created_at
- observation_time
- region

### slicks
- id
- investigation_id
- geometry
- area
- confidence
- observation_time
- source_image

### drift_runs
- id
- investigation_id
- model
- direction
- start_time
- end_time
- parameters
- uncertainty
- result_geometry

### source_regions
- id
- investigation_id
- geometry
- estimated_time
- uncertainty_radius
- confidence

### vessels
- mmsi
- name
- metadata

### ais_positions
- id
- mmsi
- timestamp
- latitude
- longitude
- speed
- course

### vessel_tracks
- id
- mmsi
- investigation_id
- geometry
- start_time
- end_time

### candidate_rankings
- id
- investigation_id
- mmsi
- spatial_score
- temporal_score
- drift_score
- behaviour_score
- data_confidence
- total_score

PostGIS shall be used for geographic geometries and spatial queries.

---

# 8. Backend Requirements

FastAPI shall expose APIs for:

```text
POST /investigations
GET  /investigations/{id}

POST /slicks/detect
GET  /investigations/{id}/slick

POST /drift/hindcast
POST /drift/forecast
GET  /investigations/{id}/drift

POST /ais/import
GET  /investigations/{id}/vessels

POST /analysis/candidates
POST /analysis/rank

GET  /investigations/{id}/source
GET  /investigations/{id}/evidence
```

API responses shall use structured JSON.

Long-running model operations should not block normal UI requests.

Redis may be used for:
- caching
- temporary processing state
- job status
- repeated query results

---

# 9. Frontend Requirements

The frontend shall use React.js and JavaScript.

MapLibre GL JS shall provide the primary geospatial visualization.

Tailwind CSS shall provide styling and layout.

The interface shall remain visually similar to the existing NEELGRIVA investigation console.

---

# 10. Investigation Console Interface

## Layout

```text
┌──────────────────────────────────────────────────────────────┐
│ NEELGRIVA                    MARITIME OIL-SPILL CONSOLE      │
├──────────────┬────────────────────────────────┬──────────────┤
│              │                                │              │
│ Investigation│                                │ Probable     │
│ State        │                                │ Source       │
│              │                                │              │
│ Layers       │            MAP                 │ Candidate    │
│              │                                │ Vessels      │
│ Controls     │                                │              │
│              │                                │ Evidence     │
│ Legend       │                                │              │
│              │                                │              │
├──────────────┴────────────────────────────────┴──────────────┤
│ Timeline / Time Slider                                      │
└──────────────────────────────────────────────────────────────┘
```

The uploaded prototype establishes the same three-column structure: left control panel, central map, right evidence/candidate panel, with a bottom timeline. fileciteturn5file0L10-L30

---

# 11. Left Panel

The left panel shall contain:

### Investigation State
Possible states:
- Region Selection
- Slick Selected
- Vessel Selected

### Layers
- Oil Probability
- Hindcast
- Forecast
- Ship Model
- AIS

### Slick Controls
- Show/Hide Slick Trajectory

### Vessel Controls
- Show/Hide Ship Trajectory

### Colour Mapping

Use a fixed semantic colour scheme similar to the existing interface:
- Oil probability: black/grey
- Hindcast: yellow
- Forecast: green
- Ship model: blue
- AIS observations: red

Probability shall control **opacity**, not the underlying category colour. The current prototype explicitly uses this behaviour. fileciteturn5file0L1-L2

---

# 12. Central Map

The central map shall display:

- Geographic base map
- Oil probability field
- Slick boundary/geometry
- Hindcast trajectory
- Forecast trajectory
- Probable source region
- Selected vessel trajectory
- AIS observations

The existing prototype uses a central map/canvas, map readout and map-state indicator. fileciteturn5file0L91-L95

Map interaction shall support:
- zoom
- pan
- layer visibility
- time selection
- slick selection
- vessel selection
- coordinate readout

---

# 13. Map Readout

When the cursor is over the map, display:

```text
Latitude
Longitude
P(oil)
```

The existing prototype displays latitude, longitude and oil probability in the map readout. fileciteturn5file0L401-L404

---

# 14. Right Panel

## Probable Source

Display:
- Source time
- Latitude
- Longitude
- Uncertainty
- Source probability region

Example:

```text
PROBABLE SOURCE

Source time       01 Sep 2026 · 02:00 UTC
Latitude          XX.XXX° N
Longitude         XX.XXX° E
Uncertainty       ± X.X km

A source probability region surrounds
this estimate. The point is not treated
as exact truth.
```

The current interface already uses this structure and explicitly states that the source point is not exact truth. fileciteturn5file0L97-L105

---

# 15. Candidate Vessel Panel

Each candidate shall display:

```text
MV Example Vessel

MMSI              XXXXXXXX
Evidence score    0.XXX

████████████
Ship Type : Oil Tanker
```

Candidates shall be sorted by SourceRank.

The interface shall allow the user to select a candidate vessel.

The current prototype uses this card-based ranking format. fileciteturn5file0L369-L378

---

# 16. Selected Vessel Evidence

Display:

- Vessel name
- MMSI
- Spatial evidence
- Temporal evidence
- Drift compatibility
- Behaviour
- Data confidence
- Overall evidence score

Example:

```text
SELECTED VESSEL EVIDENCE

Vessel              MV Example Vessel
MMSI                XXXXXXXX
Type                Oil Tanker

Spatial evidence    0.81
Temporal evidence   0.76
Drift compatibility 0.88
Behaviour           0.62

Evidence score is heuristic, not a
calibrated probability or legal finding.
```

The existing prototype uses the same evidence categories and explicitly identifies the score as heuristic rather than a legal finding. fileciteturn5file0L379-L386

---

# 17. Timeline

The interface shall provide a time slider.

Requirements:
- selectable investigation time
- map updates when time changes
- slick position updates
- trajectory display updates
- source estimate updates
- vessel/AIS display updates

The current prototype uses a 0–24 hour timeline with a selectable time value. fileciteturn5file0L407-L410

For the real system, the timeline shall use actual investigation timestamps rather than fixed demonstration hours.

---

# 18. Frontend State Model

Minimum application states:

```text
REGION
  ↓
SLICK
  ↓
VESSEL
```

### REGION
Show:
- oil probability
- map
- time control

### SLICK
Show:
- slick geometry
- hindcast
- forecast
- probable source
- candidate vessels

### VESSEL
Show:
- selected vessel
- vessel trajectory
- AIS observations
- evidence breakdown

The existing prototype follows this state progression. fileciteturn5file0L338-L351

---

# 19. Performance Requirements

The system should:
- keep map interaction responsive
- avoid blocking the UI during long-running model operations
- cache reusable results
- process AIS data in batches
- use spatial database queries where appropriate
- allow model jobs to run asynchronously

---

# 20. Security Requirements

The system shall:
- validate uploaded files
- validate API inputs
- authenticate protected deployments
- restrict access to sensitive AIS datasets
- preserve data provenance
- record investigation changes
- prevent arbitrary file execution through uploads
- avoid exposing internal database credentials to the frontend

---

# 21. Data Provenance

Every major result should retain:
- source dataset
- acquisition/observation time
- processing timestamp
- model/version
- relevant parameters
- confidence
- uncertainty

This is required for reproducibility and investigation auditability.

---

# 22. Testing Requirements

Testing shall cover:

### Unit Testing
- coordinate conversion
- spatial distance
- geometry operations
- score calculations
- probability/uncertainty calculations

### Model Testing
- SAR detection
- segmentation quality
- drift reconstruction
- anomaly detection

### Integration Testing
- SAR → detection
- detection → drift
- drift → AIS
- AIS → ranking
- ranking → frontend

### UI Testing
- layer controls
- timeline
- slick selection
- candidate selection
- evidence display
- map interaction

### Failure Testing
- missing AIS
- missing environmental data
- poor SAR quality
- no candidate vessels
- multiple equally plausible candidates
- model failure

---

# 23. Prototype Requirements

The first working prototype must demonstrate this complete chain:

```text
SAR / controlled SAR input
        ↓
Slick detection
        ↓
Slick geometry
        ↓
Environmental data
        ↓
Backward drift
        ↓
Probable source
        ↓
Historical AIS
        ↓
Candidate vessels
        ↓
Evidence analysis
        ↓
SourceRank
        ↓
Explainable result
```

Synthetic or controlled data may be used during development, but it must be explicitly labelled as synthetic/controlled.

The prototype must never present simulated results as real-world observations.

---

# 24. Definition of Done

A feature is complete only when:

- backend implementation exists
- frontend integration exists where required
- data format is defined
- errors are handled
- output is explainable
- uncertainty is represented where applicable
- test case exists
- documentation exists
- feature works through the actual application interface

---

# 25. Required End-to-End Demonstration

The final demonstration shall show:

1. Open investigation
2. View SAR-derived slick
3. Select slick
4. View slick geometry
5. Run/view backward hindcast
6. Display probable source region
7. View forward forecast
8. Load historical AIS
9. Display candidate vessels
10. Select candidate
11. Display vessel trajectory
12. Display AIS observations
13. Display evidence breakdown
14. Display SourceRank
15. Display uncertainty/confidence
16. Explain why the highest-ranked vessel is only a probable candidate

---

# 26. System Principle

NEELGRIVA shall answer:

> **“Which vessel is the most plausible source given the available evidence, and how strong is that evidence?”**

It shall not answer:

> **“Which vessel is legally guilty?”**

The final system is an evidence-analysis and decision-support platform, not an autonomous legal attribution system.

Research sources
https://elib.dlr.de/203269/1/TaylorFrancis_Yang.OpenDrift
https://www.sciencedirect.com/science/article/abs/pii/S0025326X1500510X
https://www.researchgate.net/publication/383175794_A_new_ship_tracing_technology_from_oil_spills_based_on_multi-source_data
https://doi.org/10.1080/014311699213596
https://www.mdpi.com/2077-1312/10/1/112