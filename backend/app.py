"""
backend/app.py
==============
Pure REST API — serves JSON only.
The frontend (frontend/index.html) is opened directly in the browser.

Run:
    python train_model.py   (first time only)
    python app.py
"""

import os, json, pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE  = os.path.dirname(__file__)
MODEL = os.path.join(BASE, "model")

app = Flask(__name__)
CORS(app)   # allow frontend HTML file to call the API

# ── Load models ────────────────────────────────────────────────────────
lin_reg  = pickle.load(open(os.path.join(MODEL, "linear_model.pkl"),  "rb"))
lin_reg2 = pickle.load(open(os.path.join(MODEL, "poly_model.pkl"),    "rb"))
poly_reg = pickle.load(open(os.path.join(MODEL, "poly_features.pkl"), "rb"))
metrics  = json.load(  open(os.path.join(MODEL, "metrics.json"),      "r"))


# ── /predict ───────────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    Request  JSON: { "hours": 6.5, "model": "linear" | "polynomial" }
    Response JSON: { "predicted_score": 82.1, "model": "...", "hours": 6.5 }
    """
    data       = request.get_json(force=True)
    hours      = float(data.get("hours", 0))
    model_type = data.get("model", "linear")

    x_input = np.array([[hours]])

    if model_type == "polynomial":
        score = float(lin_reg2.predict(poly_reg.transform(x_input))[0])
    else:
        score = float(lin_reg.predict(x_input)[0])

    score = round(max(0.0, min(100.0, score)), 2)

    return jsonify({"predicted_score": score, "model": model_type, "hours": hours})


# ── /metrics ───────────────────────────────────────────────────────────
@app.route("/metrics", methods=["GET"])
def get_metrics():
    return jsonify(metrics)


# ── /health ────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
