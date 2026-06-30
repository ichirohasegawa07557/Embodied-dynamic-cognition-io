from dataclasses import dataclass
import numpy as np

@dataclass
class SensorReading:
    step: int
    observed_distance_cm: float
    raw_value: float
    sensor_name: str = "distance_sensor"

class SimulatedDistanceSensor:
    def __init__(self, noise_std=0.8, seed=42):
        self.noise_std = float(noise_std)
        self.rng = np.random.default_rng(seed)

    def read(self, step: int, true_distance_cm: float) -> SensorReading:
        observed = float(true_distance_cm + self.rng.normal(0.0, self.noise_std))
        return SensorReading(step, observed, observed)
