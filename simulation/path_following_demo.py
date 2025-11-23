import time
import numpy as np
import matplotlib.pyplot as plt

from amr_core.integration.data_pipeline import IntegrationPipeline, SensorPacket


def simulate_path_following(total_time: float = 10.0, dt: float = 0.05):
    steps = int(total_time / dt)
    pipeline = IntegrationPipeline(dt=dt)

    xs, ys = [], []
    xs_ref, ys_ref = [], []
    latencies = []

    true_state = np.array([0.0, 0.0, 0.0])
    v_true = 0.8
    omega_true = 0.2

    for _ in range(steps):
        t0 = time.time()

        x, y, theta = true_state
        x += dt * v_true * np.cos(theta)
        y += dt * v_true * np.sin(theta)
        theta += dt * omega_true
        true_state = np.array([x, y, theta])

        noise = np.random.randn(3) * np.array([0.02, 0.02, 0.01])
        meas = true_state + noise

        packet = SensorPacket(
            v=v_true,
            omega=omega_true,
            meas_x=meas[0],
            meas_y=meas[1],
            meas_theta=meas[2],
        )

        state_est, _ = pipeline.step(packet)
        ref_traj = pipeline.planner.generate_path(state_est, pipeline.current_goal)
        ref_state = ref_traj[0, :]

        xs.append(state_est[0])
        ys.append(state_est[1])
        xs_ref.append(ref_state[0])
        ys_ref.append(ref_state[1])

        latencies.append((time.time() - t0) * 1000.0)

    return np.array(xs), np.array(ys), np.array(xs_ref), np.array(ys_ref), np.array(latencies)


def main():
    xs, ys, xs_ref, ys_ref, latencies = simulate_path_following()

    fig1, ax1 = plt.subplots()
    ax1.plot(xs_ref, ys_ref, label="Reference")
    ax1.plot(xs, ys, label="Estimated")
    ax1.set_xlabel("x [m]")
    ax1.set_ylabel("y [m]")
    ax1.set_title("Trajectory Tracking (Reference vs Estimated)")
    ax1.legend()
    ax1.grid(True)
    fig1.tight_layout()

    fig2, ax2 = plt.subplots()
    ax2.plot(latencies)
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Latency [ms]")
    ax2.set_title("Integration Pipeline Latency Profile")
    ax2.grid(True)
    fig2.tight_layout()

    out_dir = "../examples/sample_results"
    import os
    os.makedirs(out_dir, exist_ok=True)
    fig1.savefig(os.path.join(out_dir, "trajectory_plot.png"), dpi=200)
    fig2.savefig(os.path.join(out_dir, "latency_profile.png"), dpi=200)
    plt.close(fig1)
    plt.close(fig2)
    print("Simulation complete. Plots saved to:", out_dir)


if __name__ == "__main__":
    main()