# Predictive Analytics Application
### Study Hours vs Exam Score Predictor

A Machine Learning web application using **Linear Regression** and **Polynomial Regression (degree=2)**,
connected to a plain HTML/CSS/JS frontend via a Flask REST API.

---

## 📁 Project Structure

```
predictive_analytics_app/
│
├── frontend/                          ← Pure HTML frontend (open in browser)
│   ├── index.html                     ← Main UI page
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js                    ← Calls Flask API, renders results
│   └── images/
│       ├── plot_linear.png            ← Auto-generated on training
│       └── plot_poly.png
│
├── backend/                           ← Flask REST API
│   ├── app.py                         ← API server (port 5000)
│   ├── train_model.py                 ← Train & save ML models
│   ├── requirements.txt
│   └── model/                         ← Saved model files (auto-generated)
│       ├── linear_model.pkl
│       ├── poly_model.pkl
│       ├── poly_features.pkl
│       └── metrics.json
│
└── data/
    ├── study_hours_vs_exam_score.csv  ← Dataset (500 rows)
    └── study_hours_exam_score.ipynb  ← Original notebook
```

---

## ⚙️ Setup & Run

### Step 1 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Train the models (only once)
```bash
python train_model.py
```
This saves model `.pkl` files and generates chart images automatically.

### Step 3 — Start the API server
```bash
python app.py
```
API runs at: `http://127.0.0.1:5000`

### Step 4 — Open the frontend
Open this file directly in your browser:
```
frontend/index.html
```
Just double-click it, or drag it into Chrome/Firefox/Edge.

---

## 🌐 API Endpoints

| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| GET    | /health    | Check server is running  |
| GET    | /metrics   | Get model R² and MSE     |
| POST   | /predict   | Get predicted exam score |

**POST /predict — Request:**
```json
{ "hours": 7.5, "model": "linear" }
```
`model` → `"linear"` or `"polynomial"`

**POST /predict — Response:**
```json
{ "predicted_score": 83.42, "model": "linear", "hours": 7.5 }
```

---

## 🧠 Models

| Model                 | Library     | Degree | R²     |
|-----------------------|-------------|--------|--------|
| Linear Regression     | scikit-learn | 1     | 0.9225 |
| Polynomial Regression | scikit-learn | 2     | 0.9225 |

---

## 📊 Dataset

- **File:** `data/study_hours_vs_exam_score.csv`
- **Rows:** 500 student records
- **Features:** `Study Hours per Week` → `Exam Score (%)`

---

*Term Submission — Predictive Analytics using Data Science*
