from dataclasses import dataclass
import numpy as np

@dataclass
class SpaceState:
    step: int
    true_distance_cm: float
    disturbance: float
    actuator_effect: float

class OneDimensionalExternalSpace:
    '''
    Simulated external space.

    action -> external state change -> next observation
    '''

    def __init__(
        self,
        initial_distance_cm=55.0,
        target_distance_cm=30.0,
        actuator_gain=0.08,
        damping=0.93,
        disturbance_scale=0.35,
        seed=42,
    ):
        self.distance = float(initial_distance_cm)
        self.target = float(target_distance_cm)
        self.actuator_gain = float(actuator_gain)
        self.damping = float(damping)
        self.disturbance_scale = float(disturbance_scale)
        self.rng = np.random.default_rng(seed)
        self.t = 0
        self.velocity = 0.0

    def step(self, action: float) -> SpaceState:
        action = float(action)
        disturbance = float(self.rng.normal(0.0, self.disturbance_scale))
        actuator_effect = -self.actuator_gain * action
        self.velocity = self.damping * self.velocity + actuator_effect + disturbance * 0.05
        self.distance = float(np.clip(self.distance + self.velocity, 5.0, 120.0))
        self.t += 1
        return SpaceState(self.t, self.distance, disturbance, actuator_effect)

    def reset(self, distance_cm=None):
        if distance_cm is not None:
            self.distance = float(distance_cm)
        self.velocity = 0.0
        self.t = 0
