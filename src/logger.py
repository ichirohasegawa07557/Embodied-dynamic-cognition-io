from pathlib import Path
import pandas as pd

class ClosedLoopLogger:
    def __init__(self):
        self.rows = []

    def append(self, state, action, true_distance_cm=None, disturbance=None):
        self.rows.append({
            "step": state.step,
            "true_distance_cm": true_distance_cm,
            "observed_distance_cm": state.observed_distance_cm,
            "estimated_distance_cm": state.estimated_distance_cm,
            "target_distance_cm": state.target_distance_cm,
            "control_error_cm": state.control_error_cm,
            "predicted_next_distance_cm": state.predicted_next_distance_cm,
            "prediction_error_cm": state.prediction_error_cm,
            "action_value": action.action_value,
            "servo_angle": action.servo_angle,
            "led_intensity": action.led_intensity,
            "reason": action.reason,
            "disturbance": disturbance,
        })

    def to_dataframe(self):
        return pd.DataFrame(self.rows)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df = self.to_dataframe()
        df.to_csv(path, index=False)
        return df
