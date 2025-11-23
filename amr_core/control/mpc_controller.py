import numpy as np


class MPCStyleController:
    """Lightweight MPC-style controller for a unicycle robot."""

    def __init__(self, dt: float = 0.05):
        self.dt = dt
        self.kp_pos = 1.2
        self.kp_theta = 1.5
        self.v_max = 1.0
        self.omega_max = 1.5

    def solve(self, current_state: np.ndarray, ref_state: np.ndarray):
        x, y, theta = current_state
        xr, yr, thetar = ref_state

        ex = xr - x
        ey = yr - y

        e_long = np.cos(theta) * ex + np.sin(theta) * ey
        e_lat = -np.sin(theta) * ex + np.cos(theta) * ey

        e_theta = (thetar - theta + np.pi) % (2 * np.pi) - np.pi

        v = self.kp_pos * e_long
        omega = self.kp_theta * e_theta + 0.5 * e_lat

        v = np.clip(v, -self.v_max, self.v_max)
        omega = np.clip(omega, -self.omega_max, self.omega_max)
        return np.array([v, omega])