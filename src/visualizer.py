from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def _save(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=170)
    plt.close()

def plot_distance_control(df, path):
    plt.figure(figsize=(9, 5))
    if "true_distance_cm" in df.columns and df["true_distance_cm"].notna().any():
        plt.plot(df["step"], df["true_distance_cm"], label="true distance")
    plt.plot(df["step"], df["observed_distance_cm"], label="observed distance")
    plt.plot(df["step"], df["estimated_distance_cm"], label="estimated distance")
    plt.plot(df["step"], df["target_distance_cm"], label="target")
    plt.xlabel("step")
    plt.ylabel("distance cm")
    plt.title("Closed-loop distance control")
    plt.grid(True, linestyle="--", linewidth=0.4)
    plt.legend()
    _save(path)

def plot_action_curve(df, path):
    plt.figure(figsize=(9, 5))
    plt.plot(df["step"], df["action_value"], label="abstract action")
    plt.plot(df["step"], df["servo_angle"], label="servo angle")
    plt.xlabel("step")
    plt.ylabel("action")
    plt.title("Action output curve")
    plt.grid(True, linestyle="--", linewidth=0.4)
    plt.legend()
    _save(path)

def plot_prediction_error(df, path):
    plt.figure(figsize=(9, 5))
    plt.plot(df["step"], df["prediction_error_cm"])
    plt.xlabel("step")
    plt.ylabel("prediction error cm")
    plt.title("Prediction error over time")
    plt.grid(True, linestyle="--", linewidth=0.4)
    _save(path)

def plot_phase(df, path):
    plt.figure(figsize=(6, 6))
    plt.scatter(df["estimated_distance_cm"], df["action_value"], s=12)
    plt.xlabel("estimated distance cm")
    plt.ylabel("action value")
    plt.title("State-action phase plot")
    plt.grid(True, linestyle="--", linewidth=0.4)
    _save(path)

def summarize(df):
    return pd.DataFrame([{
        "final_abs_control_error_cm": float(abs(df["control_error_cm"].iloc[-1])),
        "mean_abs_control_error_cm": float(df["control_error_cm"].abs().mean()),
        "mean_abs_prediction_error_cm": float(df["prediction_error_cm"].abs().mean()),
        "n_steps": len(df),
    }])

def create_all_plots(log_path, results_dir="results"):
    results_dir = Path(results_dir)
    df = pd.read_csv(log_path)
    plot_distance_control(df, results_dir / "distance_control_curve.png")
    plot_action_curve(df, results_dir / "action_curve.png")
    plot_prediction_error(df, results_dir / "prediction_error_curve.png")
    plot_phase(df, results_dir / "state_phase_plot.png")
    summary = summarize(df)
    summary.to_csv(results_dir / "summary_metrics.csv", index=False)
    return summary
