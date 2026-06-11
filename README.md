# Global Supply Chain Shock Intelligence Platform

A Django web application for modeling global supply chain disruptions across **Oil**, **Semiconductor**, and **Rare Earth** shock scenarios. The platform includes interactive simulation, risk mapping, consumer impact analysis, investment intelligence, and AI-powered CEO report generation.

---

## Features

This app includes the following capabilities:

- **Executive Summary Generator** — AI-powered CEO reports using the Groq API and `llama-3.1-8b-instant`.
- **Investment Intelligence Dashboard** — Sector-level BUY / HOLD / SELL guidance with confidence scores and return projections.
- **Consumer Impact Analyzer** — Product-focused price increase and shortage risk analysis by shock category.
- **Supply Chain Risk Map** — Interactive world map showing country risk levels for each shock.
- **Shock Simulator** — Live scenario modeling with severity slider, price impact, shortage probability, and GDP impact.
- **Export Results** — Download simulations and CEO reports as **PDF** or **CSV**.
- **Dashboard Overview** — Aggregated risk summary, recent simulations, and recent CEO reports.

---

## Quick Start

### 1. Set up environment

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key (optional — for CEO reports)

```bash
copy .env.example .env
```

Edit `.env` and add your Groq key:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

Get a free key at [console.groq.com](https://console.groq.com).

**Important:** After editing `.env`, restart the server:
```bash
python manage.py runserver
```

### 4. Initialize database

```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Run the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## Export Results

You can export both simulation runs and generated CEO reports as **PDF** or **CSV**:

| Location | Export |
|----------|--------|
| **Shock Simulator** | Export current scenario results |
| **CEO Report** | Export after generation or from history |
| **Dashboard** | Export links available on recent items |

**Simulation exports include:** key shock metrics, affected countries, timeline, consumer impact, and investment recommendations.

**CEO report exports include:** full AI-generated briefing and metadata.

---

## Pages

| URL | Page |
|-----|------|
| `/` | Dashboard |
| `/simulator/` | Shock Simulator |
| `/risk-map/` | Supply Chain Risk Map |
| `/consumer-impact/` | Consumer Impact Analyzer |
| `/investment/` | Investment Intelligence Dashboard |
| `/ceo-report/` | Executive Summary Generator |
| `/admin/` | Django Admin |

---

## Tech Stack

- **Backend:** Python, Django 4.2, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js
- **Maps:** Leaflet.js
- **AI:** Groq API (`llama-3.1-8b-instant`)

---

## Project Structure

```
Task/
├── manage.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md       ← Full technical docs
├── .env.example
├── supply_chain/          # Django project settings
└── intelligence/          # Main app
    ├── models.py          # Database models
    ├── views.py           # Page views & API endpoints
    ├── exporters.py       # PDF & CSV export utilities
    ├── data.py            # Hardcoded impact data
    ├── templates/         # HTML templates
    └── static/            # CSS & JavaScript
```

---

## Admin Access

```bash
python manage.py createsuperuser
```

Then visit **http://127.0.0.1:8000/admin/**

---

## Notes

- All impact data is **hardcoded** in `intelligence/data.py` — no external datasets required.
- CEO reports require a valid `GROQ_API_KEY` in `.env`.
- The CEO report feature uses `llama-3.1-8b-instant` by default.
- Restart the server after updating `.env`.
