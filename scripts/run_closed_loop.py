import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.closed_loop import run_simulation, run_hardware_loop
from src.serial_io import SerialHardwareInterface
from src.visualizer import create_all_plots

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["simulation", "hardware"], default="simulation")
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--port", type=str, default="/dev/tty.usbmodem1101")
    parser.add_argument("--baud-rate", type=int, default=115200)
    parser.add_argument("--target-distance", type=float, default=30.0)
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    if args.mode == "simulation":
        df = run_simulation(steps=args.steps, target_distance_cm=args.target_distance)
    else:
        interface = SerialHardwareInterface(args.port, args.baud_rate)
        try:
            df = run_hardware_loop(interface, steps=args.steps, target_distance_cm=args.target_distance)
        finally:
            interface.close()

    log_path = Path("logs/closed_loop_log.csv")
    df.to_csv(log_path, index=False)
    summary = create_all_plots(log_path, "results")
    print("log saved:", log_path)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
