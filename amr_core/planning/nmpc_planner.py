import numpy as np


class SimpleNMPCPlanner:
    """Planner that generates a smooth reference between current pose and goal."""

    def __init__(self, horizon: int = 30):
        self.horizon = horizon

    def generate_path(self, start_state: np.ndarray, goal: np.ndarray):
        x0, y0, _ = start_state
        xg, yg = goal
        xs = np.linspace(x0, xg, self.horizon)
        ys = np.linspace(y0, yg, self.horizon)
        thetas = np.arctan2(np.gradient(ys), np.gradient(xs))
        return np.stack([xs, ys, thetas], axis=1)