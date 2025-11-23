from dataclasses import dataclass
import numpy as np

from amr_core.perception.ekf_fusion import EKFFusion
from amr_core.localization.vio_module import SimpleVIO
from amr_core.planning.nmpc_planner import SimpleNMPCPlanner
from amr_core.control.mpc_controller import MPCStyleController


@dataclass
class SensorPacket:
    v: float
    omega: float
    meas_x: float
    meas_y: float
    meas_theta: float


class IntegrationPipeline:
    """Integration pipeline wiring perception, localization, planning, and control."""

    def __init__(self, dt: float = 0.05):
        self.dt = dt
        self.ekf = EKFFusion(dt=dt)
        self.vio = SimpleVIO(dt=dt)
        self.planner = SimpleNMPCPlanner(horizon=30)
        self.controller = MPCStyleController(dt=dt)
        self.current_goal = np.array([2.0, 2.0])

    def step(self, sensor: SensorPacket):
        u = np.array([sensor.v, sensor.omega])

        self.ekf.predict(u)
        z = np.array([sensor.meas_x, sensor.meas_y, sensor.meas_theta])
        self.ekf.update(z)
        state_est = self.ekf.get_state()

        self.vio.propagate(u)

        ref_traj = self.planner.generate_path(state_est, self.current_goal)
        ref_state = ref_traj[0, :]

        control_cmd = self.controller.solve(state_est, ref_state)
        return state_est, control_cmd