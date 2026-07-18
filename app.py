"""Open_Geochem: a minimal, reproducible geochemical anomaly workflow."""
from __future__ import annotations

import io

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import IsolationForest
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import RobustScaler

st.set_page_config(page_title="Open_Geochem", page_icon="🌍", layout="wide")


def demo_data(seed: int = 42, n: int = 260) -> pd.DataFrame:
    """Create a deterministic exploration-geochemistry example dataset."""
    rng = np.random.default_rng(seed)
    x, y = rng.uniform(0, 100, n), rng.uniform(0, 80, n)
    centres = np.array([[30, 55], [72, 27], [58, 62]])
    influence = sum(np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 180) for cx, cy in centres)
    base = lambda mean, noise, response: np.maximum(0.01, mean + response * influence + rng.normal(0, noise, n))
    return pd.DataFrame({
        "X": x, "Y": y,
        "Cu_ppm": base(32, 8, 130), "Au_ppb": base(2.5, 0.8, 15),
        "Mo_ppm": base(3.5, 1.2, 21), "Pb_ppm": base(18, 5, 48),
        "Zn_ppm": base(65, 16, 62),
    })


def run_workflow(frame: pd.DataFrame, features: list[str], contamination: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run robust scaling, Isolation Forest anomaly detection, and explainability."""
    x = np.log1p(frame[features].clip(lower=0))
    scaled = RobustScaler().fit_transform(x)
    model = IsolationForest(contamination=contamination, random_state=42, n_estimators=300)
    prediction = model.fit_predict(scaled)
    result = frame.copy()
    result["anomaly_score"] = -model.decision_function(scaled)
    result["classification"] = np.where(prediction == -1, "Anomaly", "Background")
    importance = permutation_importance(model, scaled, -prediction, n_repeats=15, random_state=42)
    ranking = pd.DataFrame({"element": features, "importance": importance.importances_mean}).sort_values("importance", ascending=False)
    return result, ranking


st.title("🌍 Open_Geochem")
st.caption("Codex-ready, reproducible geochemical anomaly screening for exploration research.")

with st.sidebar:
    st.header("Scientific question")
    prompt = st.text_area("Describe your goal", "Identify multi-element Cu–Au–Mo anomalies and export an interpretable target map.")
    contamination = st.slider("Expected anomaly proportion", 0.02, 0.20, 0.06, 0.01)
    upload = st.file_uploader("Upload CSV (optional)", type="csv")

frame = pd.read_csv(upload) if upload else demo_data()
candidate_features = [c for c in frame.columns if c not in {"X", "Y"} and pd.api.types.is_numeric_dtype(frame[c])]
features = st.multiselect("Analysis variables", candidate_features, default=candidate_features)

if not {"X", "Y"}.issubset(frame.columns):
    st.error("CSV must include X and Y coordinate columns.")
    st.stop()
if not features:
    st.info("Choose at least one analytical variable.")
    st.stop()

results, ranking = run_workflow(frame, features, contamination)
st.success("Workflow generated: log transform → robust scaling → anomaly detection → driver ranking → export")

left, right = st.columns([1.7, 1])
with left:
    fig = px.scatter(results, x="X", y="Y", color="anomaly_score", symbol="classification", hover_data=features,
                     color_continuous_scale="Turbo", title="Geochemical anomaly score map")
    fig.update_layout(height=510, coloraxis_colorbar_title="Score")
    st.plotly_chart(fig, use_container_width=True)
with right:
    bar = px.bar(ranking, x="importance", y="element", orientation="h", title="Variables driving anomaly classification")
    bar.update_layout(height=510, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(bar, use_container_width=True)

st.subheader("Transparent research record")
st.code(f"""# User request\n{prompt}\n\n# Reproducible configuration\nrandom_state = 42\ncontamination = {contamination}\nfeatures = {features}\nmethod = 'IsolationForest + permutation importance'\n""", language="python")

csv = results.to_csv(index=False).encode("utf-8")
st.download_button("Download anomaly results (CSV)", csv, "open_geochem_anomaly_results.csv", "text/csv")
st.download_button("Download reproducibility record", io.BytesIO(ranking.to_csv(index=False).encode()), "open_geochem_feature_ranking.csv", "text/csv")
