# 🏎️ RaceEngineerAI

**AI-Powered Formula 1 Race Strategy Optimization Platform**

RaceEngineerAI is a full-stack machine learning and AI application that simulates Formula 1 race strategy decisions using real telemetry data. The platform predicts lap times using machine learning, evaluates race strategies through simulation and optimization, and provides AI-generated race engineer briefings through a conversational interface.

Built as a portfolio project by **Ishan Meduri** (B.Tech Information Technology, Manipal Institute of Technology Bengaluru) to demonstrate skills in Machine Learning, Data Engineering, Backend Development, AI Integration, and Full-Stack Engineering.

---

## 🚀 Features

### 📊 Lap Time Prediction

* Trained on real Formula 1 telemetry data using FastF1
* Predicts race lap times based on:

  * Track
  * Driver
  * Tire Compound
  * Lap Number
  * Tire Life
  * Stint Number

### 🏁 Race Strategy Simulation

* Simulates complete race stints lap-by-lap
* Models tire degradation over race distance
* Estimates total race time for custom strategies

### ⚡ Strategy Optimization

* Evaluates all valid 1-stop and 2-stop race strategies
* Ranks strategies by projected race time
* Returns top-performing strategies

### 🤖 AI Race Engineer

Powered by Google Gemini 2.5 Flash:

* Generates race strategy briefings
* Explains simulation results
* Answers race strategy questions conversationally

### 📈 Interactive Dashboard

* Dark-themed Formula 1 inspired UI
* Real-time charts and visualizations
* Strategy comparison tools
* AI engineer chat interface

---

## 🏗️ Architecture

```text
React Frontend
       │
       ▼
 FastAPI Backend
       │
 ├── ML Prediction Engine (XGBoost)
 ├── Strategy Optimizer
 ├── Race Simulator
 └── Gemini AI Integration
```

---

## 🧠 Machine Learning Pipeline

### Model

* Algorithm: XGBoost Regressor
* Framework: Scikit-learn Pipeline
* Encoding: OneHotEncoder via ColumnTransformer

### Dataset

* 12,061 race laps
* 12 Formula 1 race sessions
* Seasons: 2023–2024

Tracks Included:

* Bahrain
* Monaco
* Silverstone
* Monza
* Spain
* Hungary

### Features

| Feature   | Description       |
| --------- | ----------------- |
| Track     | Circuit name      |
| Driver    | Driver identifier |
| Compound  | Tire compound     |
| LapNumber | Current lap       |
| TyreLife  | Tire age          |
| Stint     | Stint number      |

### Validation

GroupKFold Cross Validation

Grouping Key:

* RaceId

This prevents data leakage between laps from the same race session.

### Results

| Metric   | Value          |
| -------- | -------------- |
| Mean MAE | 1.535 seconds  |
| Std Dev  | ±0.568 seconds |

### Key Modeling Decisions

✅ Race sessions only (qualifying excluded)

✅ Safety car laps removed

✅ Sector times excluded to avoid target leakage

✅ Tire degradation learned through TyreLife feature instead of hardcoded assumptions

---

## 🛠️ Tech Stack

### Machine Learning

* FastF1
* XGBoost
* Scikit-learn
* Pandas
* NumPy
* Joblib

### Backend

* FastAPI
* Uvicorn
* Pydantic
* Python-dotenv

### AI

* Google Gemini 2.5 Flash

### Frontend

* React
* Vite
* Axios
* Recharts

---

## 📂 Project Structure

```text
race-engineer-ai/
│
├── core/
│   ├── config.py
│   │
│   ├── data/
│   │   ├── fetch.py
│   │   └── features.py
│   │
│   ├── models/
│   │   ├── laptime_model.py
│   │   └── degradation.py
│   │
│   └── optimizer.py
│
├── api/
│   ├── app.py
│   ├── schemas.py
│   └── ai.py
│
├── scripts/
│   └── train.py
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Header.jsx
│       │   ├── StrategyForm.jsx
│       │   ├── StrategyResults.jsx
│       │   ├── LapTimeChart.jsx
│       │   └── AIEngineer.jsx
│       │
│       └── api/
│           └── client.js
│
└── models_store/
    └── laptime_model.joblib
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Returns application health status.

---

### Race Simulation

```http
POST /simulate
```

Simulates lap-by-lap race pace for a given strategy.

---

### Compound Comparison

```http
POST /compare
```

Compares projected performance between tire compounds.

---

### Strategy Optimization

```http
POST /optimize
```

Returns top 5 race strategies ranked by total race time.

---

### AI Strategy Briefing

```http
POST /explain
```

Generates a race engineer style strategy explanation using Gemini.

---

### AI Chat

```http
POST /chat
```

Conversational race engineer assistant.

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/itsh-29/race-engineer-ai.git

cd race-engineer-ai
```

### Backend Setup

```bash
python -m venv venv

source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run backend:

```bash
uvicorn api.app:app --reload
```

Backend:

```text
http://localhost:8000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 📸 Dashboard Highlights

* Strategy Optimization Dashboard
* Lap Time Visualization Charts
* Compound Comparison Analytics
* AI Race Engineer Chat
* Natural Language Strategy Briefings

---

## 📌 Current Status

| Component          | Status         |
| ------------------ | -------------- |
| ML Pipeline        | ✅ Complete     |
| Model Training     | ✅ Complete     |
| Backend APIs       | ✅ Complete     |
| Strategy Optimizer | ✅ Complete     |
| Gemini Integration | ✅ Complete     |
| React Frontend     | ✅ Complete     |
| Deployment         | 🚧 In Progress |

Deployment Targets:

* Backend → Render
* Frontend → Vercel

---

## 🔮 Roadmap (v2.0)

### Planned Features

* Driver photos
* Team-specific color themes
* Full 2023–2025 race calendar
* Year selector
* Circuit layout visualizations
* Weather effects
* Track temperature modeling
* Authentication & user profiles
* Saved strategy history
* Shareable strategy reports

---

## 🎯 Learning Outcomes

This project demonstrates:

* Machine Learning Pipelines
* Feature Engineering
* Time-Series Sports Analytics
* FastAPI Development
* REST API Design
* AI Application Integration
* React Frontend Development
* Data Visualization
* End-to-End Deployment

---

## 👨‍💻 Author

**Ishan Meduri**

B.Tech Information Technology
Manipal Institute of Technology Bengaluru

GitHub: https://github.com/itsh-29

Project Repository:
https://github.com/itsh-29/race-engineer-ai

---

## 📄 License

This project is licensed under the MIT License.
