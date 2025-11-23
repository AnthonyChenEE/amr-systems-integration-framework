# MPC Formulation (Simplified)

We consider a unicycle-like model and a horizon-based quadratic cost on
position and heading error. The implementation in this repository uses
a lightweight proportional law wrapped in an MPC-style interface so that
it can later be replaced with a full optimizer.