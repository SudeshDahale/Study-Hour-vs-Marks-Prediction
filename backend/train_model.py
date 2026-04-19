"""
backend/train_model.py
======================
Run this ONCE before starting the server.
Trains Linear & Polynomial Regression models and saves:
  - model/linear_model.pkl
  - model/poly_model.pkl
  - model/poly_features.pkl
  - model/metrics.json
  - ../frontend/images/plot_linear.png
  - ../frontend/images/plot_poly.png
"""

import os, json, pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error

BASE     = os.path.dirname(__file__)
CSV      = os.path.join(BASE, "..", "data", "study_hours_vs_exam_score.csv")
MODEL    = os.path.join(BASE, "model")
IMG_DIR  = os.path.join(BASE, "..", "frontend", "images")

os.makedirs(MODEL,   exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# ── Load dataset ──────────────────────────────────────────────────────
dataset = pd.read_csv(CSV)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
print(f"Loaded {len(dataset)} rows  |  columns: {list(dataset.columns)}")

# ── Linear Regression ─────────────────────────────────────────────────
lin_reg = LinearRegression()
lin_reg.fit(x, y)
lin_r2  = r2_score(y, lin_reg.predict(x))
lin_mse = mean_squared_error(y, lin_reg.predict(x))
print(f"Linear     R²={lin_r2:.4f}  MSE={lin_mse:.4f}")

# ── Polynomial Regression (degree=2) ──────────────────────────────────
poly_reg = PolynomialFeatures(degree=2)
x_poly   = poly_reg.fit_transform(x)
lin_reg2 = LinearRegression()
lin_reg2.fit(x_poly, y)
poly_r2  = r2_score(y, lin_reg2.predict(x_poly))
poly_mse = mean_squared_error(y, lin_reg2.predict(x_poly))
print(f"Polynomial R²={poly_r2:.4f}  MSE={poly_mse:.4f}")

# ── Save models ───────────────────────────────────────────────────────
pickle.dump(lin_reg,  open(os.path.join(MODEL, "linear_model.pkl"),   "wb"))
pickle.dump(lin_reg2, open(os.path.join(MODEL, "poly_model.pkl"),     "wb"))
pickle.dump(poly_reg, open(os.path.join(MODEL, "poly_features.pkl"),  "wb"))

metrics = {
    "linear":     {"r2": round(lin_r2,  4), "mse": round(lin_mse,  4)},
    "polynomial": {"r2": round(poly_r2, 4), "mse": round(poly_mse, 4)},
}
json.dump(metrics, open(os.path.join(MODEL, "metrics.json"), "w"), indent=2)
print("Models + metrics.json saved.")

# ── Generate chart images ─────────────────────────────────────────────
x_line = np.linspace(x.min(), x.max(), 300).reshape(-1, 1)

plt.figure(figsize=(7, 4))
plt.scatter(x, y, color="#ef4444", alpha=0.55, s=18, label="Data points")
plt.plot(x_line, lin_reg.predict(x_line), color="#3b82f6", linewidth=2.2, label=f"Linear fit  (R²={lin_r2:.3f})")
plt.title("Study Hours vs Exam Score — Linear Regression", fontsize=12, pad=10)
plt.xlabel("Study Hours per Week"); plt.ylabel("Exam Score (%)")
plt.legend(); plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "plot_linear.png"), dpi=110)
plt.close()

plt.figure(figsize=(7, 4))
plt.scatter(x, y, color="#ef4444", alpha=0.55, s=18, label="Data points")
plt.plot(x_line, lin_reg2.predict(poly_reg.transform(x_line)), color="#8b5cf6", linewidth=2.2, label=f"Poly fit  (R²={poly_r2:.3f})")
plt.title("Study Hours vs Exam Score — Polynomial Regression (deg=2)", fontsize=12, pad=10)
plt.xlabel("Study Hours per Week"); plt.ylabel("Exam Score (%)")
plt.legend(); plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "plot_poly.png"), dpi=110)
plt.close()

print("Charts saved to frontend/images/")
print("✓  Training complete.")
