from src.environment import OneDimensionalExternalSpace
from src.sensors import SimulatedDistanceSensor
from src.state_estimator import MemoryStateEstimator
from src.controller import PIDCognitiveController
from src.logger import ClosedLoopLogger

def run_simulation(
    steps=240,
    seed=42,
    target_distance_cm=30.0,
    initial_distance_cm=55.0,
    sensor_noise_std=0.8,
):
    env = OneDimensionalExternalSpace(
        initial_distance_cm=initial_distance_cm,
        target_distance_cm=target_distance_cm,
        seed=seed,
    )
    sensor = SimulatedDistanceSensor(noise_std=sensor_noise_std, seed=seed + 1)
    estimator = MemoryStateEstimator(target_distance_cm=target_distance_cm)
    controller = PIDCognitiveController()
    logger = ClosedLoopLogger()

    previous_action = 0.0

    for _ in range(steps):
        space_state = env.step(previous_action)
        reading = sensor.read(space_state.step, space_state.true_distance_cm)
        internal = estimator.update(
            step=reading.step,
            observed_distance_cm=reading.observed_distance_cm,
            previous_action=previous_action,
        )
        action = controller.decide(internal)
        logger.append(
            internal,
            action,
            true_distance_cm=space_state.true_distance_cm,
            disturbance=space_state.disturbance,
        )
        previous_action = action.action_value

    return logger.to_dataframe()

def run_hardware_loop(interface, steps=240, target_distance_cm=30.0):
    estimator = MemoryStateEstimator(target_distance_cm=target_distance_cm)
    controller = PIDCognitiveController()
    logger = ClosedLoopLogger()
    previous_action = 0.0

    for _ in range(steps):
        reading = interface.read_sensor()
        internal = estimator.update(reading.step, reading.distance_cm, previous_action)
        action = controller.decide(internal)
        interface.send_action(action.servo_angle, action.led_intensity)
        logger.append(internal, action)
        previous_action = action.action_value

    return logger.to_dataframe()
