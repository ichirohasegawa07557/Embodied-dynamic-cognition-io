.PHONY: setup test simulate replay app clean

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

test:
	python -m pytest -q

simulate:
	python scripts/run_closed_loop.py --mode simulation --steps 240

replay:
	python scripts/replay_logs.py --log logs/closed_loop_log.csv

app:
	streamlit run app.py

clean:
	rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
