# Global Supply Chain Shock Intelligence Platform — Documentation

Complete technical reference for the SCSI platform: architecture, setup, features, data models, APIs, and configuration.

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Application Features](#application-features)
6. [Data Layer](#data-layer)
7. [Database Models](#database-models)
8. [API Reference](#api-reference)
9. [Frontend & Static Assets](#frontend--static-assets)
10. [Admin Panel](#admin-panel)
11. [Project Structure](#project-structure)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The **Global Supply Chain Shock Intelligence Platform (SCSI)** is a Django 4.2 web application for modeling and analyzing global supply chain disruptions. It simulates three shock categories — **Oil**, **Semiconductor**, and **Rare Earth** — and provides risk mapping, consumer impact analysis, investment guidance, and AI-generated executive reports.

### Key Design Principles

- **Hardcoded data only** — All impact metrics, country profiles, and sector recommendations live in `intelligence/data.py`. No external datasets or live market feeds are required.
- **SQLite database** — Lightweight persistence for simulations and CEO reports.
- **Responsive dark UI** — Navy sidebar layout works on desktop and mobile.
- **Optional AI integration** — CEO reports use the Groq API when a key is configured.

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Django 4.2 |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js 4.4 |
| Maps | Leaflet.js 1.9 |
| AI | Groq API (`llama3-8b-8192`) |
| Config | python-dotenv |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser (Client)                      │
│  HTML Templates │ CSS │ JS (Chart.js, Leaflet, Fetch API)   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│                    Django (intelligence app)                 │
│  Views ──► data.py (hardcoded logic)                         │
│       ──► models.py (SQLite persistence)                     │
│       ──► Groq API (CEO reports only)                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         db.sqlite3              Groq Cloud API
```

### Request Flow — Shock Simulator

1. User selects shock type and adjusts severity slider.
2. JavaScript calls `GET /api/impact/?shock=oil&severity=75`.
3. `calculate_shock_impact()` in `data.py` computes metrics.
4. UI updates price impact, shortage probability, timeline, and affected countries.
5. On "Run & Save", `POST /simulator/run/` persists a `ShockSimulation` record.

### Request Flow — CEO Report

1. User selects shock type and severity, clicks **Generate CEO Report**.
2. JavaScript sends `POST /ceo-report/generate/` with JSON body.
3. View builds a structured prompt from impact, consumer, and sector data.
4. Groq API returns an executive briefing.
5. Report is saved to `CEOReport` model and displayed in the UI.

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Internet access (for Chart.js, Leaflet CDN, and Groq API)

### Step-by-Step Setup

```bash
# 1. Clone or navigate to project directory
cd Task

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux

# 6. Apply database migrations
python manage.py migrate

# 7. Seed hardcoded reference data
python manage.py seed_data

# 8. (Optional) Create admin superuser
python manage.py createsuperuser

# 9. Start development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Configuration

### Environment Variables (`.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | For CEO reports | API key from [console.groq.com](https://console.groq.com) |

Example `.env`:

```
GROQ_API_KEY=gsk_your_api_key_here
```

### Django Settings (`supply_chain/settings.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `GROQ_API_KEY` | From `.env` | Groq authentication |
| `GROQ_MODEL` | `llama3-8b-8192` | LLM model for CEO reports |
| `GROQ_API_URL` | Groq chat completions endpoint | API URL |
| `DEBUG` | `True` | Development mode |
| `DATABASES` | SQLite (`db.sqlite3`) | Database backend |

---

## Application Features

### 1. Dashboard (`/`)

Overview page showing:

- Baseline metrics (price impact, shortage probability, countries at risk, GDP impact)
- Shock category cards linking to the simulator
- Top 6 risk countries by score
- Recent simulations and CEO reports from the database

### 2. Shock Simulator (`/simulator/`)

Interactive scenario modeling:

- **Shock types:** Oil, Semiconductor, Rare Earth
- **Severity slider:** 0–100%
- **Live metrics:** Price increase %, shortage probability, GDP impact, affected country count
- **Timeline:** Four-phase disruption progression (Week 1–2 through Month 4–6)
- **Country impact bars:** Top affected nations ranked by exposure
- **Save simulation:** Persists results to SQLite

**Impact formula:**

```
factor = severity / 50
price_increase = base_price_impact × factor
shortage_probability = min(99, base_shortage_prob × factor)
gdp_impact = price_increase × 0.35
country_impact = country_exposure × (severity / 100)
```

Countries are flagged as "affected" when `country_impact >= 25`.

### 3. World Risk Map (`/risk-map/`)

Interactive Leaflet map with:

- **15 countries** as color-coded circle markers
- **Risk levels:** Low (green), Medium (yellow), High (orange), Critical (red)
- **Popups:** Risk score, exposure percentages, summary text
- **Filter tabs:** Switch shock context (Oil / Semiconductor / Rare Earth)
- **Data table:** Full country risk index below the map

Map tiles use CartoDB Dark Matter for consistency with the UI theme.

### 4. Consumer Impact (`/consumer-impact/`)

Product-level impact cards showing:

- **Price increase %** with visual progress bar
- **Shortage probability %** with risk badge (Low / Moderate / High)
- **6 products per shock type** (e.g., Gasoline, Smartphones, Electric Vehicles)

Filter by shock type and severity via form controls.

### 5. Investment Dashboard (`/investment/`)

Sector-level investment guidance:

- **Recommendations:** BUY, HOLD, or SELL per sector
- **Confidence score:** 0–100%
- **Expected 12-month return:** Percentage
- **Rationale:** Text explanation per sector

**Charts (Chart.js):**

- Doughnut chart — BUY / HOLD / SELL distribution
- Horizontal bar chart — Expected returns by sector

**6 sectors per shock type** (18 total recommendations seeded).

### 6. CEO Report Generator (`/ceo-report/`)

AI-powered executive briefings:

- Select shock type and severity
- Generates structured report via Groq API with sections:
  - Executive Summary
  - Risk Assessment
  - Consumer Impact
  - Investment Implications
  - Recommended Actions
- Reports saved to database with history view
- Requires valid `GROQ_API_KEY`

---

## Data Layer

All scenario data is defined in `intelligence/data.py`.

### Shock Types

| Slug | Name | Base Price Impact (at 50%) | Base Shortage Prob (at 50%) |
|------|------|---------------------------|----------------------------|
| `oil` | Oil Supply Shock | 18.5% | 42% |
| `semiconductor` | Semiconductor Shock | 24.0% | 55% |
| `rare_earth` | Rare Earth Shock | 31.0% | 48% |

### Countries (15)

United States, China, Russia, Saudi Arabia, Taiwan, South Korea, Japan, Germany, India, Australia, Brazil, United Kingdom, Vietnam, Indonesia, Chile.

Each country includes: coordinates, risk level, risk score (0–100), exposure percentages for all three shock types, and a summary.

### Consumer Products (6 per shock)

Examples:

- **Oil:** Gasoline, Diesel, Airline Tickets, Food (Transport-linked)
- **Semiconductor:** Smartphones, Laptops, New Vehicles, Gaming Consoles
- **Rare Earth:** Electric Vehicles, Wind Turbines, Industrial Magnets

### Sector Recommendations (6 per shock)

Examples:

- **Oil:** Energy (BUY), Transportation (SELL), Materials (BUY)
- **Semiconductor:** Semiconductors (BUY), Automotive (SELL), Healthcare (BUY)
- **Rare Earth:** Materials (BUY), Clean Energy (SELL), Defense (BUY)

### Seeding Data

```bash
python manage.py seed_data
```

Populates `ShockType`, `CountryRisk`, and `SectorRecommendation` tables from `data.py`.

---

## Database Models

### ShockType

| Field | Type | Description |
|-------|------|-------------|
| slug | CharField | `oil`, `semiconductor`, `rare_earth` |
| name | CharField | Display name |
| description | TextField | Shock description |
| base_price_impact | FloatField | Base price increase % at severity 50 |
| base_shortage_prob | FloatField | Base shortage probability at severity 50 |

### CountryRisk

| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Country name |
| code | CharField | 3-letter code (e.g., USA) |
| latitude / longitude | FloatField | Map coordinates |
| risk_level | CharField | low, medium, high, critical |
| risk_score | IntegerField | 0–100 |
| oil_exposure | FloatField | Oil exposure % |
| semiconductor_exposure | FloatField | Semiconductor exposure % |
| rare_earth_exposure | FloatField | Rare earth exposure % |
| summary | TextField | Risk summary text |

### SectorRecommendation

| Field | Type | Description |
|-------|------|-------------|
| sector | CharField | Sector name |
| shock_type | CharField | Associated shock |
| recommendation | CharField | BUY, HOLD, or SELL |
| confidence | IntegerField | 0–100 |
| expected_return | FloatField | 12-month return % |
| rationale | TextField | Explanation |

### ShockSimulation

| Field | Type | Description |
|-------|------|-------------|
| shock_type | CharField | Shock slug |
| severity | IntegerField | 0–100 |
| price_increase_pct | FloatField | Calculated price impact |
| shortage_probability | FloatField | Calculated shortage prob |
| affected_countries | IntegerField | Count of affected nations |
| gdp_impact_pct | FloatField | GDP impact estimate |
| results_json | JSONField | Full impact payload |
| created_at | DateTimeField | Timestamp |

### CEOReport

| Field | Type | Description |
|-------|------|-------------|
| shock_type | CharField | Shock slug |
| severity | IntegerField | 0–100 |
| report_content | TextField | Generated report text |
| created_at | DateTimeField | Timestamp |

---

## API Reference

### GET `/api/impact/`

Calculate shock impact without saving.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `shock` | string | `oil` | `oil`, `semiconductor`, or `rare_earth` |
| `severity` | integer | `50` | 0–100 |

**Response:**

```json
{
  "impact": {
    "shock_type": "oil",
    "shock_name": "Oil Supply Shock",
    "severity": 75,
    "price_increase_pct": 27.8,
    "shortage_probability": 63.0,
    "gdp_impact_pct": 9.73,
    "affected_countries": [...],
    "affected_count": 12,
    "timeline": [...]
  },
  "consumer": [...],
  "sectors": [...]
}
```

### POST `/simulator/run/`

Run and persist a simulation.

**Headers:** `Content-Type: application/json`, `X-CSRFToken: <token>`

**Body:**

```json
{
  "shock_type": "semiconductor",
  "severity": 60
}
```

**Response:**

```json
{
  "id": 1,
  "impact": { ... },
  "message": "Simulation saved successfully"
}
```

### POST `/ceo-report/generate/`

Generate an AI executive report.

**Headers:** `Content-Type: application/json`, `X-CSRFToken: <token>`

**Body:**

```json
{
  "shock_type": "rare_earth",
  "severity": 80
}
```

**Response:**

```json
{
  "id": 1,
  "report": "## Executive Summary\n...",
  "shock_type": "rare_earth",
  "severity": 80
}
```

**Error (no API key):**

```json
{
  "error": "GROQ_API_KEY not configured. Add it to your .env file."
}
```

### GET `/simulator/export/<format>/`

Export the current simulation scenario without saving.

**Formats:** `csv`, `pdf`

**Query Parameters:** `shock`, `severity`

**Example:** `/simulator/export/pdf/?shock=oil&severity=75`

**CSV sections:** Scenario summary, affected countries, timeline, consumer impact, investment recommendations.

**PDF sections:** Key metrics table, affected countries, consumer impact table, sector recommendations.

### GET `/simulator/export/<id>/<format>/`

Export a saved simulation by database ID.

**Example:** `/simulator/export/3/csv/`

### GET `/ceo-report/export/<id>/<format>/`

Export a saved CEO report.

**Example:** `/ceo-report/export/1/pdf/`

**CSV:** Metadata plus full report text.

**PDF:** Formatted executive report with section headers and bullet points.

---

## Frontend & Static Assets

### Templates (`intelligence/templates/intelligence/`)

| Template | Purpose |
|----------|---------|
| `base.html` | Layout shell with navy sidebar navigation |
| `dashboard.html` | Home overview |
| `shock_simulator.html` | Interactive simulator |
| `risk_map.html` | Leaflet world map |
| `consumer_impact.html` | Product impact cards |
| `investment.html` | Sector recommendations + charts |
| `ceo_report.html` | AI report generator |

### Static Files (`intelligence/static/intelligence/`)

| File | Purpose |
|------|---------|
| `css/style.css` | Full dark navy theme, responsive layout |
| `js/main.js` | Sidebar toggle for mobile |
| `js/simulator.js` | Live slider updates, simulation save |
| `js/risk_map.js` | Leaflet map initialization and markers |
| `js/investment.js` | Chart.js doughnut and bar charts |
| `js/ceo_report.js` | Groq report generation and formatting |

### External CDN Dependencies

- Leaflet CSS/JS 1.9.4 (unpkg)
- Chart.js 4.4.1 (jsdelivr)
- CartoDB Dark Matter map tiles

---

## Admin Panel

Access at **http://127.0.0.1:8000/admin/** after creating a superuser.

Manageable models:

- Shock Types
- Country Risks
- Sector Recommendations
- Shock Simulations
- CEO Reports

```bash
python manage.py createsuperuser
```

---

## Project Structure

```
Task/
├── manage.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
├── .env.example
├── .env
├── db.sqlite3
├── supply_chain/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── intelligence/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── data.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py
    ├── templates/
    │   └── intelligence/
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── shock_simulator.html
    │       ├── risk_map.html
    │       ├── consumer_impact.html
    │       ├── investment.html
    │       └── ceo_report.html
    └── static/
        └── intelligence/
            ├── css/
            │   └── style.css
            └── js/
                ├── main.js
                ├── simulator.js
                ├── risk_map.js
                ├── investment.js
                └── ceo_report.js
```

---

## Troubleshooting

### CEO Report shows "API Key Required"

Add your Groq key to `.env`:

```
GROQ_API_KEY=gsk_your_key_here
```

Restart the development server after editing `.env`.

### Map not displaying

Ensure you have internet access. Leaflet and map tiles load from CDN. Check browser console for blocked requests.

### Charts not rendering

Chart.js loads from jsdelivr CDN. Verify network connectivity and that JavaScript is enabled.

### `ModuleNotFoundError: No module named 'django'`

Activate the virtual environment and install dependencies:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Database errors after model changes

```bash
python manage.py makemigrations intelligence
python manage.py migrate
python manage.py seed_data
```

### Static files not loading in production

For production deployment, run:

```bash
python manage.py collectstatic
```

And configure your web server to serve the `staticfiles` directory.

---

## License & Notes

This is a demonstration/educational project. All impact data is simulated and hardcoded — not sourced from live market or geopolitical feeds. Do not use generated reports or investment recommendations for real financial decisions.

For full technical details, see source files in the `intelligence/` app. For a quick start guide, see [README.md](README.md).
