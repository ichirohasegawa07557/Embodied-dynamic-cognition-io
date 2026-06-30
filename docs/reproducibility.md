# Reproducibility

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Test

```bash
python -m pytest -q
```

## Simulation

```bash
python scripts/run_closed_loop.py --mode simulation --steps 240
```

## Viewer

```bash
streamlit run app.py
```
