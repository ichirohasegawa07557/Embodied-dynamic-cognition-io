from dataclasses import dataclass

@dataclass
class InternalState:
    step: int
    observed_distance_cm: float
    estimated_distance_cm: float
    predicted_next_distance_cm: float
    prediction_error_cm: float
    target_distance_cm: float
    control_error_cm: float

class MemoryStateEstimator:
    '''
    Memory-based state estimator.
    '''

    def __init__(self, target_distance_cm=30.0, alpha=0.35):
        self.target = float(target_distance_cm)
        self.alpha = float(alpha)
        self.estimate = None
        self.previous_prediction = None

    def update(self, step: int, observed_distance_cm: float, previous_action: float = 0.0) -> InternalState:
        observed = float(observed_distance_cm)

        if self.estimate is None:
            self.estimate = observed
            self.previous_prediction = observed

        prediction_error = observed - float(self.previous_prediction)
        self.estimate = self.alpha * observed + (1.0 - self.alpha) * self.estimate
        predicted_next = self.estimate - 0.08 * float(previous_action)
        self.previous_prediction = predicted_next
        control_error = self.estimate - self.target

        return InternalState(
            int(step),
            observed,
            float(self.estimate),
            float(predicted_next),
            float(prediction_error),
            self.target,
            float(control_error),
        )
