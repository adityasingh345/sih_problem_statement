# National Weather Big Data Analytics Platform — SIH 26069 MVP

Local-only, runnable hackathon prototype for weather incident intelligence. It uses seeded mock data only; no third-party feeds or APIs are called.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r backend/requirements.txt
.venv/bin/uvicorn backend.main:app --reload --port 8000
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api` to FastAPI.

## What it demonstrates

- One global date, event, state, city and verification-status filter applied to KPIs, map, tables and analytics.
- 60 seeded reports across 15 incidents and 12 Indian locations (1–12 September 2026).
- Deterministic event/location/severity classification, TF-IDF duplicate matching, credibility scoring and verification scoring.
- Simulated live incoming reports, with an optional 7-second auto mode. All changes occur without a refresh.
- Offline coordinate map fallback, so map interaction remains useful when tiles are unavailable.

## Local data

`backend/data/reports.json`, `incidents.json`, `weather.json`, and `incoming_reports.json` are generated deterministically by `backend/seed_data.py` and are committed as local data artifacts after its first run.

## Future roadmap (not implemented)

IMD feeds, social-media ingestion, IndicBERT/XLM-R, image/video verification, satellite/radar data, Kafka/Spark pipelines, hyperlocal nowcasting, automated alerts, and WhatsApp/IVR reporting.
