import numpy as np

from src.environment import OneDimensionalExternalSpace
from src.sensors import SimulatedDistanceSensor
from src.state_estimator import MemoryStateEstimator
from src.controller import PIDCognitiveController
from src.closed_loop import run_simulation
from src.visualizer import summarize

def test_environment_step():
    env = OneDimensionalExternalSpace(seed=1)
    s = env.step(0.0)
    assert s.true_distance_cm > 0
    assert s.step == 1

def test_sensor_reading():
    sensor = SimulatedDistanceSensor(seed=1)
    r = sensor.read(1, 30.0)
    assert r.step == 1
    assert isinstance(r.observed_distance_cm, float)

def test_state_estimator():
    est = MemoryStateEstimator(target_distance_cm=30.0)
    state = est.update(1, 35.0, previous_action=0.0)
    assert state.control_error_cm > 0

def test_controller_output_bounds():
    est = MemoryStateEstimator(target_distance_cm=30.0)
    state = est.update(1, 60.0, previous_action=0.0)
    controller = PIDCognitiveController()
    action = controller.decide(state)
    assert 20 <= action.servo_angle <= 160
    assert 0 <= action.led_intensity <= 255

def test_simulation_dataframe():
    df = run_simulation(steps=20, seed=2)
    assert len(df) == 20
    assert "observed_distance_cm" in df.columns
    assert "action_value" in df.columns

def test_summary_metrics():
    df = run_simulation(steps=20, seed=3)
    summary = summarize(df)
    assert "mean_abs_control_error_cm" in summary.columns

def test_control_changes_over_time():
    df = run_simulation(steps=40, seed=4)
    assert df["action_value"].abs().sum() > 0

def test_prediction_error_exists():
    df = run_simulation(steps=40, seed=5)
    assert np.isfinite(df["prediction_error_cm"]).all()

def test_reason_labels_exist():
    df = run_simulation(steps=10, seed=6)
    assert df["reason"].notna().all()
