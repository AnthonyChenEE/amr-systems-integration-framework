# Architecture Overview

Layers:
- Perception (EKF-style fusion)
- Localization (VIO-style dead reckoning)
- Planning (simple horizon planner)
- Control (MPC-style controller)
- Integration (pipeline that connects all modules)