import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.visualizer import create_all_plots

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=str, default="logs/closed_loop_log.csv")
    parser.add_argument("--results-dir", type=str, default="results")
    args = parser.parse_args()

    summary = create_all_plots(args.log, args.results_dir)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
