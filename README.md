# Autonomous Mobile Robot Systems Integration Framework  
A modular, end-to-end autonomy stack for perception, localization, planning, control, and systems integration.
<img width="1024" height="1024" alt="amr" src="https://github.com/user-attachments/assets/2b7d9516-72e6-4d28-b7ce-efee8157dbd3" />

---

> ## **Note for Recruiters & Engineering Teams**
> This repository was developed to demonstrate competence in **full-stack robotics and autonomy systems integration**,  
> inspired by the architectural patterns used in advanced robotics platforms  
> (e.g., Tesla Optimus / AMR, factory automation robots, and large-scale autonomous systems).
>
> It highlights practical engineering abilities in:  
> - Multi-sensor perception & EKF fusion  
> - VIO-style localization  
> - Nonlinear/MPC-inspired trajectory planning  
> - Real-time mobile robot control  
> - Deterministic, timing-safe integration pipelines  
>
> If you are reviewing this project as part of a job application,  
> this work reflects my interest in building **reliable, scalable, and elegantly engineered autonomous robotic systems**.

---

# 📌 Overview

This repository implements a lightweight but extensible **autonomous mobile robot (AMR) autonomy stack**,  
designed to mirror the architecture commonly used in real industrial robotics systems.

The stack includes:

- **Perception:** EKF-based pose fusion  
- **Localization:** VIO-style dead-reckoning  
- **Planning:** Nonlinear MPC-inspired horizon planner  
- **Control:** MPC-style tracking controller  
- **Integration:** Real-time pipeline orchestrating the full loop  
- **Simulation:** A reproducible demo of trajectory tracking and latency profiling  

This project is fully standalone and written to be easy to read, extend, and deploy.

---

# ⚡ Technical Highlights (Tesla-Style Focus)

### ✅ **1. True Full-Stack Autonomy Architecture**
```
Sensors → Perception → Localization → Planning → Control → Actuation
          ↑______________________________________________↓
                    Real-Time Integration Layer
```

### ✅ **2. Deterministic Integration Pipeline**
- lock-free data flow  
- deterministic timing hooks  
- structured sensor packets  
- consistent world/body frame conventions  

### ✅ **3. EKF-Based Multi-Sensor Fusion**
- prediction & update  
- covariance propagation  
- measurement innovation  

### ✅ **4. VIO-Style Dead-Reckoning Localization**
- lightweight pose propagation  
- IMU/odometry compatible  

### ✅ **5. Nonlinear / MPC-Inspired Planning**
- horizon-based references  
- smooth heading generation  

### ✅ **6. MPC-Style Tracking Controller**
- heading/lateral error  
- input saturation  
- short-horizon receding control  

### ✅ **7. Simulation-to-Real Friendly Design**
- trajectory plots  
- latency profiling  
- reproducible workflow  

---

# 🖥️ System Diagram
See: `docs/system_diagram.png`

---

# 🚀 Running the Simulation
```
python simulation/path_following_demo.py
```

Produces:
- `trajectory_plot.png`  
- `latency_profile.png`  

---

# 📁 Repository Structure
```
amr_core/
docs/
simulation/
examples/
```

---

# 📝 License
MIT License.

---

# 👤 Author
**Yuanzhe (Anthony) Chen**  
UNSW Sydney – Autonomous Systems, MPC, Robotics, AMR Integration
