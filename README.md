# Digital Twin for Industrial Pump Remaining Useful Life (Simulation)

This project showcases a **Digital Twin** solution for **Condition-Based Monitoring (CBM)** and **Prognostics** of critical industrial assets—specifically centrifugal pumps used in energy and water treatment sectors.

Unlike traditional approaches that rely on historical data or AI, this simulation uses a **physics-based mathematical model** to forecast pump health, enabling robust, real-time demonstrations and validation.

---

## Project Objective

The goal is to transition from costly scheduled downtime (**Preventive Maintenance**) or unexpected breakdowns (**Reactive Maintenance**) to intelligent **Condition-Based Monitoring**.

The Digital Twin enables this by:

- **Modeling Degradation:** Simulates exponential wear of key components (e.g., bearing fatigue).
- **Calculating RUL:** Computes the **Remaining Useful Life (RUL)** in real-time.
- **Triggering Alerts:** Issues notifications when RUL drops below a safe threshold.

This simulation provides a clear demonstration of the financial and safety benefits of advanced monitoring, particularly in the Energy Industry (e.g., nuclear and gas power plants) where centrifugal pumps are mission-critical.

Critical Assets: Centrifugal pumps are vital for cooling, feedwater, and lubrication systems, making their failure highly consequential.

Avoided Costs: By successfully modeling and forecasting the time of failure, this system demonstrates the capacity to prevent catastrophic unplanned outages, which can save millions in potential downtime and significantly minimize safety risks.

Data Validation: The simulation environment can be used to validate assumptions about component lifespan, providing the necessary justification for the complexity and cost of deploying comprehensive, advanced CBM systems in real-world facilities.

---

## Technical Details & Features

| Feature              | Component             | Description |
|----------------------|-----------------------|-------------|
| **Physics Model**     | `pump_simulator.py`   | Implements an **Exponential Degradation Formula** ($A (1 - e^{-kt})$) applied to sensor values like $\text{Vibration}$, $\text{Temperature}$, and $\text{Current}$. |
| **Real-Time Stream**  | `simulation_app.py`   | Simulates a live $\text{IoT}$ sensor feed by importing data and RUL from the simulator. |
| **Visualization**     | Streamlit             | Interactive web interface to visualize **Actual RUL** and sensor trends over time. |
| **Prognostics Output**| Streamlit Alert       | Displays a **CRITICAL ALERT** when RUL falls below the $\mathbf{50}$-hour threshold, signaling the need for intervention. |

---
## Screenshots
<img width="2534" height="784" alt="image" src="https://github.com/user-attachments/assets/c5365a42-6dca-4e04-9aa6-10d1d1019941" />
<img width="2413" height="1079" alt="image" src="https://github.com/user-attachments/assets/6974e19d-5ce7-4cdf-96a1-784e7052ddc4" />
<img width="2486" height="1045" alt="image" src="https://github.com/user-attachments/assets/bffb682d-a15f-4a19-8596-c2f0cd08aab5" />

