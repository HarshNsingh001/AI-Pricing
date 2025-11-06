# AI‑Powered Menu Pricing System

This project implements a dynamic pricing engine for menu items based on:

* Internal factors (current price & competitor prices)
* External factors (weather & nearby events)
* Rule‑based logic with optional ML fallback
* Persistent storage of pricing requests, recommendations, weather snapshots, and event snapshots

Built entirely in **Python (FastAPI)** with a clean REST architecture and proper database persistence.

---

## ✅ Features

✔ Dynamic price recommendation endpoint (`POST /api/pricing/suggest`)
✔ Internal + external factor weighting
✔ Weather & event signals influence demand multipliers
✔ Competitor price ingestion (`POST /api/ingest/competitors`)
✔ SQLite/PostgreSQL compatible
✔ Swagger documentation
✔ Graceful fallback if external APIs fail
✔ Database snapshots for future analytics
✔ Auto‑creation of menu items when ingesting competitor data
✔ Exception handling with rollback safety

---

## 🧠 Pricing Logic Overview

1. **Internal factors**

   * Current menu price
   * Median competitor price
   * Internal weight multiplier

2. **External factors**

   * Weather condition demand boosts
   * Temperature‑based elasticity
   * Event popularity & distance decay multiplier

3. **Output**

   * Recommended price
   * Weight breakdown
   * Human‑readable reasoning

---

## 📦 Tech Stack

**Backend:** FastAPI (Python)
**ORM:** SQLAlchemy
**DB:** SQLite (default) or PostgreSQL
**AI:** Rule‑based model + optional scikit‑learn regression
**Docs:** Swagger (built‑in)

---

## 📁 Project Structure

```
ai-pricing-engine/
├── app/
│   ├── routers/
│   │   ├── pricing.py
│   │   └── ingest.py
│   ├── pricing_engine/
│   │   ├── rules.py
│   │   └── ml.py
│   ├── services/
│   │   ├── weather_client.py
│   │   └── events_client.py
│   ├── models.py
│   ├── schemas.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### 1️⃣ Clone / Extract

Open folder in VS Code:

```
File → Open Folder → ai-pricing-engine
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ (Optional) Install dotenv loader

```
pip install python-dotenv
```

### 4️⃣ Create `.env` file in root

```
DATABASE_URL=sqlite:///./local.db
OWM_API_KEY=YOUR_OPEN_WEATHER_KEY
TICKETMASTER_API_KEY=YOUR_TICKETMASTER_KEY
```

### 5️⃣ Run Server

```
uvicorn app.main:app --reload
```

### 6️⃣ Open Swagger UI

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Example Request (manual externals)

```json
{
  "menu_item_id": 123,
  "current_price": 250,
  "competitor_prices": [240, 260, 245],
  "weather": { "temperature": 32, "condition": "Sunny" },
  "events": [ { "name": "Food Festival", "popularity": "High", "distance_km": 2.5 } ]
}
```

### ✅ Example Response

```json
{
  "menu_item_id": 123,
  "recommended_price": 268,
  "factors": {
    "internal_weight": 0.6,
    "external_weight": 0.4
  },
  "reasoning": "Higher demand expected due to warm weather and nearby high‑popularity event."
}
```

---

## 🧬 Competitor Ingestion

Endpoint auto‑creates missing menu items.

```json
{
  "menu_item_id": 123,
  "competitor_prices": [248, 251, 255]
}
```

Response:

```json
{ "status": "ok", "menu_item_id": 123, "inserted": 3 }
```

---

## 🔐 Health Check

Run:

```
GET /health
```

You will see:

```json
{
  "status": "ok",
  "db": "sqlite",
  "owm_key_loaded": true,
  "tm_key_loaded": true
}
```

---

## 🏗️ Architectural Overview

```
           ┌─────────────────────────────────┐
           │        Client (Swagger/UI)       │
           └──────────────┬──────────────────┘
                          │HTTP
                          ▼
                 ┌──────────────────┐
                 │     FastAPI       │
                 └───────┬──────────┘
                         │Routers
            ┌────────────┴──────────────┐
            │                           │
            ▼                           ▼
   /api/pricing/suggest        /api/ingest/competitors
            │                           │
            │ Pricing Engine             │Save competitor prices
            ▼                           │Auto create MenuItem
   ┌─────────────────────────┐          │
   │   Rule/ML blending      │          │
   │ Temperature elasticity   │          │
   │ Event distance decay     │          │
   └───────┬─────────────────┘          │
           │Store snapshots              │
           ▼                             │
         Database (SQLite/Postgres) ◄────┘
```

---

### 🧩 Senior Design Choices

* Data snapshots provide **auditability** & future ML training
* Rule-engine fallback ensures reliability if ML fails
* External factors decoupled for easy swapping of providers
* DB schema supports trend analysis downstream

---

## 🛠️ Engineering Trade‑offs (Intentionally Considered)

* Not over‑engineering ML training pipeline (scope control)
* No external task queue (FaaS complexity avoided)
* Rule engine transparent for interviewer reasoning
* SQLite default avoids infra friction for reviewer

---

## 📸 Working Proof (Screenshots) (Screenshots)

Below are execution proofs from Swagger UI while testing the assignment:

> ✅ Server running successfully
> ✅ Endpoints responding with correct payloads
> ✅ Database persistence operational
> ✅ Manual weather/event testing stable

*(Screenshots attached separately with submission)*

---

## 🔥 Error Handling

* DB insert failures → rollback
* External API failures → graceful fallback
* Missing fields → pydantic validation
* Missing menu items → auto‑create

---

## 📚 Future Improvements

🔁 **Temporal price smoothing** to avoid sudden spikes
📊 **Daily trend modeling** for heat‑map demand curves
🎯 **Category‑level elasticity learning** (burgers vs beverages)
🧠 **Model retraining trigger** based on error threshold
🛰️ **Granular event scoring** based on popularity tiers & timing
👥 **Crowd density signals** from footfall APIs

---

## 🧪 Technical Decisions

**Why FastAPI?**

* Async‑ready, excellent typing, built‑in docs

**Why rule+ML hybrid?**

* Deterministic fallback, interpretable outputs

**Why snapshot persistence?**

* Enables historical regression & explainability

**Why weighted logic?**

* Explicit tunable control over internal/external influence

---

* Time‑of‑day surge modifiers
* Historical demand learning
* Menu category elasticity modeling
* Event timestamps & duration awareness
* Real competitor ingestion scraping
* Price smoothing to avoid volatility

---

## 🗂 Why SQLite ?

* Easy to run locally
* Zero‑install friction
* Portable for interview evaluation

PostgreSQL is supported via `DATABASE_URL` switch.

---

## 🧾 Notes

* Tested thoroughly using Swagger UI
* Graceful error handling added intentionally
* External signals snapshotted for audit
* Lightweight ML integration behind the scenes

---

## 👤 Author

Harsh Narayan Singh

---

## ✅ Final Status

Everything tested end‑to‑end:

* ✅ Pricing suggestions
* ✅ Competitor ingestion
* ✅ Snapshot persistence
* ✅ Swagger interactions
* ✅ Environment variable loading
