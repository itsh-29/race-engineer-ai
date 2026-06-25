# 🏎️ RaceEngineerAI – Formula 1 Strategy Simulator

RaceEngineerAI is an AI-powered telemetry analysis and race strategy simulation system built using real Formula 1 data.
It analyzes driver performance, predicts lap times, and simulates race strategies such as tire choices and pit stop decisions.

---

## 🚀 Features

* 📊 Telemetry Analysis using real F1 data (FastF1)
* ⏱️ Lap Time Prediction using Machine Learning
* 🧠 Strategy Simulation (multi-lap + tire degradation)
* 🔄 Pit Stop Strategy Comparison (1-stop vs no-stop)
* 📉 Lap Time Degradation Visualization
* 📊 Strategy Comparison Graphs

---

## 🧠 Tech Stack

* Python
* FastF1
* Pandas
* NumPy
* Scikit-learn
* Matplotlib

---

## 📊 Sample Outputs

### Lap Time Degradation

![Lap Time Comparison](lap_time_comparison.png)

---

### Strategy Comparison

![Strategy Comparison](strategy_comparison.png)

---

## 🏎️ Example Simulation

```
Track: Monaco

Soft → Medium (1-stop): 1450.2s  
Medium only (no stop): 1440.8s  

→ No-stop strategy wins
```

---

## ⚙️ How It Works

1. Collects real F1 telemetry data using FastF1
2. Cleans and processes lap data
3. Trains a Random Forest model to predict lap times
4. Simulates tire degradation over multiple laps
5. Evaluates race strategies including pit stops
6. Visualizes results using graphs

---

## 📁 Project Structure

```
race-engineer-ai/
│
├── data_pipeline/
│   └── fetch_data.py
│
├── ml_models/
│   ├── train_model.py
│   └── strategy_simulator.py
│
├── lap_time_comparison.png
├── strategy_comparison.png
└── README.md
```

---

## 🔥 Future Improvements

* 🌐 Web dashboard (FastAPI + React)
* 🧠 AI race engineer assistant
* 📈 Real-time telemetry analysis
* 🏁 Full race simulation with pit strategies

---

## 👨‍💻 Author

Built by Ishan Meduri
BTech IT | AI/ML Enthusiast

---

## ⭐ Why This Project?

This project goes beyond basic machine learning by combining:

* Real-world data
* Predictive modeling
* Strategy simulation

It mimics real Formula 1 race engineering workflows and decision-making.

---
