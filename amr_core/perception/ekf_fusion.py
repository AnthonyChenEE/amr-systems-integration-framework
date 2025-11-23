import numpy as np


class EKFFusion:
    """Minimal EKF-style fusion for planar pose.

    State: [x, y, theta]
    Control: [v, omega]
    """

    def __init__(self, dt: float = 0.05):
        self.dt = dt
        self.x = np.zeros(3)
        self.P = np.eye(3) * 0.1
        self.Q = np.diag([1e-3, 1e-3, 1e-4])
        self.R = np.diag([5e-2, 5e-2, 2e-2])

    def predict(self, u: np.ndarray):
        v, omega = u
        x, y, theta = self.x
        dt = self.dt

        x_pred = x + dt * v * np.cos(theta)
        y_pred = y + dt * v * np.sin(theta)
        theta_pred = theta + dt * omega
        self.x = np.array([x_pred, y_pred, theta_pred])

        Fx = np.array(
            [
                [1.0, 0.0, -dt * v * np.sin(theta)],
                [0.0, 1.0, dt * v * np.cos(theta)],
                [0.0, 0.0, 1.0],
            ]
        )
        self.P = Fx @ self.P @ Fx.T + self.Q

    def update(self, z: np.ndarray):
        H = np.eye(3)
        y = z - H @ self.x
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (np.eye(3) - K @ H) @ self.P

    def get_state(self) -> np.ndarray:
        return self.x.copy()