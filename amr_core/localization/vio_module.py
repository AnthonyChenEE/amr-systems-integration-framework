import numpy as np


class SimpleVIO:
    """Very lightweight VIO-style dead reckoning."""

    def __init__(self, dt: float = 0.05):
        self.dt = dt
        self.state = np.zeros(3)

    def propagate(self, u: np.ndarray):
        v, omega = u
        x, y, theta = self.state
        dt = self.dt

        x_new = x + dt * v * np.cos(theta)
        y_new = y + dt * v * np.sin(theta)
        theta_new = theta + dt * omega
        self.state = np.array([x_new, y_new, theta_new])

    def get_pose(self) -> np.ndarray:
        return self.state.copy()