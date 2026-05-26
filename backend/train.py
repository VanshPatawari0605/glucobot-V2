import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

# ── 1. Load Data ─────────────────────────────────────────────────────────────
print("=" * 60)
print("  GlucoBot — Model Training Pipeline")
print("=" * 60)

df = pd.read_csv("data/diabetes.csv")
print(f"\n[DATA] Loaded {len(df)} rows, {df.shape[1]} columns")
print(f"[DATA] Class distribution:\n{df['Outcome'].value_counts().to_string()}")

# ── 2. Clean Data ────────────────────────────────────────────────────────────
zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df[zero_cols] = df[zero_cols].replace(0, np.nan)
for col in zero_cols:
    df[col] = df[col].fillna(df[col].median())

print(f"\n[CLEAN] Replaced 0s with median in: {zero_cols}")

# ── 3. Feature Engineering ───────────────────────────────────────────────────
df['BMI_Age']              = df['BMI'] * df['Age']
df['Glucose_Insulin']      = df['Glucose'] * df['Insulin']
df['Glucose_BMI']          = df['Glucose'] * df['BMI']
df['Glucose_Age']          = df['Glucose'] / (df['Age'] + 1)
df['Insulin_Resistance']   = df['Insulin'] / (df['Glucose'] + 1)
df['BMI_Category']         = (df['BMI'] >= 30).astype(int)  # obese flag

print(f"[FEATURES] Added 6 engineered features")
print(f"[FEATURES] Final feature count: {df.shape[1] - 1}")

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# ── 4. SMOTE Balancing ───────────────────────────────────────────────────────
sm = SMOTE(random_state=42)
X, y = sm.fit_resample(X, y)
print(f"\n[SMOTE] After balancing: {dict(zip(*np.unique(y, return_counts=True)))}")

# ── 5. Train/Test Split ──────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 6. Scale ─────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
print(f"[SPLIT] Train: {len(X_train)} | Test: {len(X_test)}")

# ── 7. Tune XGBoost with RandomizedSearchCV ──────────────────────────────────
print("\n[XGB TUNING] Running RandomizedSearchCV (50 iterations, 5-fold CV)...")

xgb_param_grid = {
    "n_estimators":      [200, 300, 400, 500],
    "learning_rate":     [0.01, 0.03, 0.05, 0.08, 0.1],
    "max_depth":         [3, 4, 5, 6, 7],
    "subsample":         [0.6, 0.7, 0.8, 0.9, 1.0],
    "colsample_bytree":  [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "reg_alpha":         [0, 0.01, 0.1, 0.5, 1.0],
    "reg_lambda":        [0.5, 1.0, 1.5, 2.0, 3.0],
    "min_child_weight":  [1, 2, 3, 5],
    "gamma":             [0, 0.1, 0.2, 0.3, 0.5],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

xgb_search = RandomizedSearchCV(
    XGBClassifier(random_state=42, eval_metric='logloss', verbosity=0),
    param_distributions=xgb_param_grid,
    n_iter=50,
    scoring='roc_auc',
    cv=cv,
    n_jobs=-1,
    random_state=42,
    verbose=1
)
xgb_search.fit(X_train_scaled, y_train)

best_xgb = xgb_search.best_estimator_
print(f"\n[XGB TUNING] Best params:\n{xgb_search.best_params_}")
print(f"[XGB TUNING] Best CV ROC-AUC: {xgb_search.best_score_:.4f}")

# ── 8. Define All Models (XGBoost = tuned) ───────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, C=0.1),
    "KNN":                 KNeighborsClassifier(n_neighbors=7),
    "Random Forest":       RandomForestClassifier(
                               n_estimators=300, max_depth=12,
                               min_samples_split=4, min_samples_leaf=2,
                               random_state=42, n_jobs=-1),
    "Gradient Boosting":   GradientBoostingClassifier(
                               n_estimators=200, learning_rate=0.05,
                               max_depth=4, random_state=42),
    "SVM":                 SVC(kernel='rbf', C=10, gamma='scale', probability=True),
    "XGBoost (Tuned)":     best_xgb,
}

# ── 9. Train & Evaluate All Models ──────────────────────────────────────────
print("\n" + "=" * 60)
print(f"  {'Model':<22} {'Accuracy':>9} {'F1':>8} {'ROC-AUC':>9} {'CV(5-fold)':>12}")
print("=" * 60)

results = {}
trained = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred  = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    acc     = accuracy_score(y_test, y_pred)
    f1      = f1_score(y_test, y_pred)
    auc     = roc_auc_score(y_test, y_proba)
    cv_mean = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='accuracy').mean()

    results[name] = {"accuracy": acc, "f1": f1, "roc_auc": auc, "cv": cv_mean}
    trained[name] = model

    print(f"  {name:<22} {acc*100:>8.2f}% {f1:>8.4f} {auc:>9.4f} {cv_mean*100:>10.2f}%")

# ── 10. Ensemble (Top 3 by ROC-AUC) ─────────────────────────────────────────
top3 = sorted(results, key=lambda n: results[n]["roc_auc"], reverse=True)[:3]
print(f"\n[ENSEMBLE] Building soft-vote ensemble from top 3: {top3}")

ensemble = VotingClassifier(
    estimators=[(n, trained[n]) for n in top3],
    voting='soft'
)
ensemble.fit(X_train_scaled, y_train)
e_pred  = ensemble.predict(X_test_scaled)
e_proba = ensemble.predict_proba(X_test_scaled)[:, 1]

e_acc = accuracy_score(y_test, e_pred)
e_f1  = f1_score(y_test, e_pred)
e_auc = roc_auc_score(y_test, e_proba)
e_cv  = cross_val_score(ensemble, X_train_scaled, y_train, cv=cv, scoring='accuracy').mean()

results["Ensemble"] = {"accuracy": e_acc, "f1": e_f1, "roc_auc": e_auc, "cv": e_cv}
trained["Ensemble"] = ensemble

print(f"  {'Ensemble':<22} {e_acc*100:>8.2f}% {e_f1:>8.4f} {e_auc:>9.4f} {e_cv*100:>10.2f}%")

# ── 11. Pick Best Model (by ROC-AUC) ─────────────────────────────────────────
best_name  = max(results, key=lambda n: results[n]["roc_auc"])
best_stats = results[best_name]

print("\n" + "=" * 60)
print(f"  Best Model : {best_name}")
print(f"  Accuracy   : {best_stats['accuracy']*100:.2f}%")
print(f"  F1 Score   : {best_stats['f1']:.4f}")
print(f"  ROC-AUC    : {best_stats['roc_auc']:.4f}")
print(f"  CV(5-fold) : {best_stats['cv']*100:.2f}%")
print("=" * 60)

print(f"\n[REPORT] Classification Report — {best_name}:")
print(classification_report(y_test, trained[best_name].predict(X_test_scaled),
                             target_names=["No Diabetes", "Diabetes"]))

# ── 12. Save ──────────────────────────────────────────────────────────────────
os.makedirs("model", exist_ok=True)
joblib.dump(trained[best_name], "model/diabetes_model.pkl")
joblib.dump(scaler,             "model/scaler.pkl")

print(f"[SAVED] model/diabetes_model.pkl  ← {best_name}")
print(f"[SAVED] model/scaler.pkl")
print("\n✅ Training complete.\n")