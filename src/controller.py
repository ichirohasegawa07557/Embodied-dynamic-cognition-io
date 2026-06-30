from dataclasses import dataclass
import numpy as np
from src.state_estimator import InternalState

@dataclass
class ActionCommand:
    step: int
    action_value: float
    servo_angle: int
    led_intensity: int
    reason: str

class PIDCognitiveController:
    '''
    Converts internal state into output action.
    '''

    def __init__(self, kp=0.42, ki=0.015, kd=0.22, action_limit=12.0):
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.action_limit = float(action_limit)
        self.integral = 0.0
        self.previous_error = 0.0

    def decide(self, state: InternalState) -> ActionCommand:
        error = state.control_error_cm
        self.integral += error
        derivative = error - self.previous_error

        raw_action = self.kp * error + self.ki * self.integral + self.kd * derivative
        action = float(np.clip(raw_action, -self.action_limit, self.action_limit))
        self.previous_error = error

        servo_angle = int(np.clip(90 + action * 4.0, 20, 160))
        led_intensity = int(np.clip(abs(error) * 8.0, 0, 255))

        if abs(error) < 1.5:
            reason = "stable_near_target"
        elif error > 0:
            reason = "distance_too_large_reduce_distance"
        else:
            reason = "distance_too_small_increase_distance"

        return ActionCommand(state.step, action, servo_angle, led_intensity, reason)

    def reset(self):
        self.integral = 0.0
        self.previous_error = 0.0
