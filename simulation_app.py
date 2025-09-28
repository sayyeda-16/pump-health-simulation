import pandas as pd
import numpy as np
import streamlit as st
import time
from pump_simulator import generate_single_pump_cycle, TOTAL_TIME_STEPS, SENSORS, BASELINES

# --- Configuration Constants ---
WINDOW_SIZE = 50
CRITICAL_THRESHOLD = 50  # Threshold for Maintenance Alert


# --- Simulation Engine ---

def run_pure_simulation():
    """
    Simulates a live pump run, calculates the true RUL, and visualizes the result.
    """
    st.header("⚙️ Real-Time Pump Health Monitoring")

    # Create a new, unseen pump degradation cycle for testing
    TEST_FAULT_START = np.random.randint(2000, 7000)
    TEST_CYCLE_ID = 999

    # Generate the full degradation data instantly (the Digital Twin pre-calculated ground truth)
    test_df = generate_single_pump_cycle(TEST_CYCLE_ID, TEST_FAULT_START)

    # DataFrame to hold the history for plotting
    history_df = pd.DataFrame(columns=['Time_Step', 'Actual_RUL', 'Vibration'])

    # Streamlit containers to update elements live
    status_text = st.empty()
    chart = st.line_chart(history_df.set_index('Time_Step'))

    st.markdown(f"**Simulation Started:** Pump Cycle {TEST_CYCLE_ID}. Degradation begins at **{TEST_FAULT_START}h**.")

    for time_step in range(TOTAL_TIME_STEPS):

        # Get the sensor readings and RUL for the current time step
        current_data = test_df.loc[(TEST_CYCLE_ID, time_step)]
        actual_rul = current_data['RUL']
        current_vibration = current_data['Vibration']

        # --- Update History and Chart ---
        if time_step % 50 == 0:  # Update every 50 hours for visualization speed

            new_row = pd.DataFrame([{
                'Time_Step': time_step,
                'Actual_RUL': actual_rul,
                'Vibration': current_vibration
            }])

            # Update Streamlit chart: Plot RUL and Vibration
            chart.add_rows(new_row.set_index('Time_Step'))

            # Update Status Box
            status = f"Time: **{time_step}h** | **RUL:** **{actual_rul:.1f}h** | **Vibration:** **{current_vibration:.2f}**"

            if actual_rul < CRITICAL_THRESHOLD:
                status_text.markdown(f"## ⚠️ CRITICAL ALERT! RUL Below {CRITICAL_THRESHOLD}h! ⚠️")
                status_text.markdown(f"**Current Status:** {status}")
            else:
                status_text.markdown(f"**Current Status:** {status}")

        # Simulate real-time stream speed
        time.sleep(0.001)


# --- App Layout ---

def main():
    st.set_page_config(page_title="Pump Health Simulation", layout="wide")
    st.title("Industrial Pump Digital Twin Simulations")

    st.markdown("""
        This application simulates the physics of pump degradation (bearing wear) in real-time. 
        It demonstrates the **Remaining Useful Life (RUL)** concept and the threshold for maintenance action.
        """)

    if st.button("Start Live Simulation"):
        st.session_state['started'] = True
        st.markdown(f"**Maintenance Threshold:** {CRITICAL_THRESHOLD} hours")
        run_pure_simulation()


if __name__ == '__main__':
    main()