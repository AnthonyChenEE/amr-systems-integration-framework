# Autonomous Mobile Robot Systems Integration Framework
## System Design Document (Engineering Draft)
**Author: Yuanzhe (Anthony) Chen**

---

# 1. Introduction

The Autonomous Mobile Robot (AMR) Systems Integration Framework was developed as an exploration of how a compact, maintainable, and production-oriented autonomy stack is structured when deployed in real engineering environments. Instead of treating perception, localization, planning, and control as isolated algorithms, the system is intentionally shaped around the interactions between these modules. This reflects an industry reality: in high-performance robotics teams—whether for factory AMRs, AGV fleets, or humanoid mobility subsystems—**integration quality determines system performance** more than the sophistication of any single algorithm.

The goal of this design was not to achieve state-of-the-art accuracy, but to demonstrate a clean, deterministic, and extensible autonomy architecture. Every component was selected and implemented to mirror principles found in industrial AMR software stacks: predictable timing, clear interfaces, minimal hidden state, and the ability to run consistently under limited compute budgets.

---

# 2. System Overview

The entire system is structured around a classic full-stack autonomy pipeline:

Sensors → Perception → Localization → Planning → Control → Actuation  
↑______________________________________________________________↓  
Real-Time Integration Layer

Each subsystem fulfills a distinct role, but none of them are meant to operate independently. The design deliberately avoids circular dependencies and keeps the data flow directional and predictable. This makes the system easy to extend—for example, adding a visual odometry module or replacing the planner with a nonlinear MPC implementation requires minimal architectural changes.

A major emphasis of the system is **consistency over complexity**. Industrial AMR teams prioritize reliability, traceability, and deterministic operation over theoretical optimality. This framework adopts the same philosophy.

---

# 3. Perception and State Estimation

## 3.1 Design Rationale

The perception layer provides the foundational estimate of the robot’s state—information required by every downstream subsystem. A lightweight Extended Kalman Filter (EKF) was chosen because it offers the right balance of simplicity, interpretability, and deterministic runtime. It maps naturally to common AMR motion models and can maintain stable performance even with limited sensor quality.

## 3.2 EKF Structure

The EKF consumes:
- control inputs *(v, ω)*  
- noisy position and heading measurements *(xₘ, yₘ, θₘ)*  

It performs:
- motion prediction  
- Jacobian-based covariance propagation  
- innovation calculation  
- measurement correction  
- output of updated state and covariance  

The architecture is intentionally simple but structured exactly like ones used in real robots—clean, traceable, and easily replaceable with a more advanced multi-sensor fusion pipeline.

## 3.3 Parallel Dead-Reckoning

A VIO-style dead-reckoning module runs in parallel to provide:
- low-latency pose propagation  
- estimator redundancy  
- drift monitoring  

Running both streams in parallel is a common practice in AMR and AGV systems. It reduces reliance on a single estimator and improves system robustness without adding significant complexity.

---

# 4. Localization Strategy

Localization is intentionally lightweight. The dead-reckoning module integrates the robot’s motion using the unicycle model at a fixed rate. Although simple, it serves two important engineering roles:

1. It provides a fast, low-latency source of motion estimates.  
2. It offers a consistency check against EKF state, enabling drift detection.

This approach mirrors early-stage robotics systems where reliability is more important than maximizing sensor sophistication.

---

# 5. Planning Framework

## 5.1 Philosophy

The planner is designed to be reliable, predictable, and computationally inexpensive. Industrial robotics teams rarely start with complex nonlinear optimization. Instead, they begin with solutions that produce consistent trajectories and integrate well with controllers.

## 5.2 Smooth Trajectory Generation

The planner generates a short-horizon trajectory by interpolating between the robot’s current state and the goal. Orientation is derived from local gradients, producing smooth and differentiable reference paths that the controller can follow without excessive oscillation.

This structure integrates naturally with MPC-style control, which prefers predictable reference evolution.

---

# 6. Control System

## 6.1 MPC-Inspired Controller

The controller uses a structure inspired by receding-horizon MPC but without solving an explicit optimization problem. It computes:
- longitudinal error  
- lateral error  
- heading error  

Based on these terms, velocity and angular velocity commands are produced with saturation. Although simple, this structure retains the key behavioral characteristics of a full MPC controller, including stability under moderate disturbances and smooth convergence.

## 6.2 Engineering Intent

The controller’s design goal is **interchangeability**. It intentionally mirrors the interface of a full MPC solver so that future upgrades (e.g., OSQP, acados) can be incorporated with minimal changes. This reflects how industrial robots evolve over time.

---

# 7. Integration Layer

The integration layer governs:
- execution ordering  
- timing consistency  
- data ownership  
- communication between subsystems  

A typical cycle performs:
1. Sensor read  
2. EKF prediction and update  
3. Dead-reckoning propagation  
4. Trajectory generation  
5. Controller computation  
6. Command dispatch  

The loop avoids blocking, dynamic allocation, and implicit state changes. This reflects real-world industrial mobility stacks, where predictability is more valuable than peak algorithmic performance.

---

# 8. Simulation and Validation

Simulation validates system behavior and timing characteristics.  
Key checks include:

- estimator stability  
- reference smoothness  
- controller convergence  
- real-time performance consistency  

Latency profiling indicates that the entire loop runs well within common embedded deadlines, even in Python. Porting the system to C++ would comfortably support control rates of 50–100 Hz.

Trajectory plots show smooth convergence without oscillation or divergence, indicating correct subsystem integration.

---

# 9. Engineering Trade-offs

Key trade-offs were intentionally made to demonstrate strong system architecture rather than algorithmic novelty:

- EKF instead of multi-sensor fusion  
- Horizon interpolation instead of nonlinear global planning  
- MPC-style controller instead of full optimization  
- No ROS2 middleware to maintain readability  

These choices reflect the priorities of early-stage AMR system bring-up, where clarity and robustness matter more than complexity.

---

# 10. Future Extensions

The architecture is intentionally extensible. Potential next steps include:

- Visual odometry integration  
- True nonlinear MPC with QP/NLP solvers  
- Obstacle constraints and dynamic avoidance  
- ROS2 migration for real robot deployment  
- Embedded deployment on Jetson / real-time x86  
- Multi-robot coordination planning  

All additions can be achieved without modifying the core architecture.

---

# 11. Conclusion

The AMR Systems Integration Framework demonstrates the principles of production-oriented autonomy system design: clean subsystem boundaries, deterministic execution, and a focus on integration over isolated algorithm development. The framework shows that **autonomy is fundamentally a systems problem**, and strongly reflects the engineering discipline required in high-performance robotics organizations.

