# Open_Geochem

**Open_Geochem** is a small, runnable prototype for AI-assisted geochemical analysis. It demonstrates a scientific workflow that starts from a plain-language research question and produces reproducible anomaly-screening outputs.

## Why it exists

Earth-science datasets are rich but difficult to connect: geological records, geochemical assays, spatial coordinates, remote sensing and environmental observations often require specialist programming. Open_Geochem is a domain-oriented interaction model for turning a question into an inspectable computational workflow—not a black-box answer.

## What the prototype demonstrates

- A natural-language geoscience task input
- CSV-based geochemical data ingestion (`X`, `Y`, plus numerical element columns)
- Log transformation and robust scaling
- Multi-element anomaly screening with Isolation Forest
- A spatial anomaly-score map and feature-importance ranking
- A visible parameter record and downloadable result files

The default dataset is synthetic and deterministic, so the entire example is reproducible. Replace it with your own CSV to explore a field dataset.

## Run locally

```bash
git clone https://github.com/YOUR-USERNAME/open-geochem.git
cd open-geochem
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Input format

Provide a CSV containing `X` and `Y` coordinate columns and one or more numeric geochemical variables, for example `Cu_ppm`, `Au_ppb`, `Mo_ppm`, `Pb_ppm`, `Zn_ppm`.

## Scientific validation note

This is a decision-support prototype. Anomaly results must be interpreted with geological context, QA/QC, sampling design, detection limits and independent verification; it does not substitute for expert geological judgment.

## Codex Devpost project

Open_Geochem explores how Codex-powered coding assistance can help researchers create, inspect and adapt reproducible geoscience workflows.

### How Codex and GPT-5.6 were used

Codex and GPT-5.6 were used as collaborative development tools to translate a geoscience workflow specification into this runnable prototype: they helped scaffold the Streamlit interface, structure the anomaly-screening pipeline, document the reproducibility controls, and refine the scientific communication. The final workflow intentionally exposes the method, variables, random seed, and downloadable outputs so that researchers can inspect and validate results rather than treat AI output as an opaque conclusion.
