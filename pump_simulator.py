import numpy as np
import pandas as pd
import os  # To save the file

# Define Constants and System Parameters
TIME_STEP_UNIT = 'hour'
TOTAL_TIME_STEPS = 10000  # Max life (e.g., 10,000 hours)
NUM_CYCLES = 200  # We will generate 200 full pump run-to-failure histories
SENSORS = ['Vibration', 'Temperature', 'Motor_Current']

BASELINES = {
    'Vibration': {'mean': 1.8, 'std': 0.15},
    'Temperature': {'mean': 52, 'std': 1.5},
    'Motor_Current': {'mean': 165, 'std': 2.0}
}

FAULT_AMPLITUDES = {
    'Vibration': 3.0,
    'Temperature': 6.0,
    'Motor_Current': 1.5
}

DEGRADATION_RATE = 0.005


def calculate_rul(total_steps, fault_start_step):
    """Calculates RUL for a single cycle."""
    time_to_fail = total_steps - np.arange(total_steps)
    max_rul = total_steps - fault_start_step
    rul = np.clip(time_to_fail, 0, max_rul)
    return rul


def generate_single_pump_cycle(cycle_id, fault_start_step, total_steps=TOTAL_TIME_STEPS):
    """Generates time-series data for one complete pump run-to-failure cycle."""

    # 1. Calculate RUL (The target variable for the AI)
    rul = calculate_rul(total_steps, fault_start_step)

    # 2. Initialize a DataFrame for the cycle
    df = pd.DataFrame({'Cycle_ID': cycle_id, 'Time_Step': np.arange(total_steps), 'RUL': rul})

    # 3. Generate Sensor Data (Baseline + Noise + Degradation)
    for sensor in SENSORS:
        baseline = BASELINES[sensor]['mean']
        noise = np.random.normal(0, BASELINES[sensor]['std'], total_steps)

        # --- Degradation Calculation ---

        # Calculate the time elapsed since the fault was initiated.
        # This will be 0 before the fault_start_step, and increase after.
        time_since_fault = np.clip(df['Time_Step'] - fault_start_step, 0, None)

        # Model degradation as an exponential growth (or "fatigue curve").
        # Degradation starts at 0 and approaches the FAULT_AMPLITUDE as time_since_fault increases.
        degradation = FAULT_AMPLITUDES[sensor] * (1 - np.exp(-DEGRADATION_RATE * time_since_fault))

        # The final sensor reading is the sum of all components
        df[sensor] = baseline + noise + degradation

    return df.set_index(['Cycle_ID', 'Time_Step'])


def generate_full_training_data(num_cycles=NUM_CYCLES):
    """
    Generates the complete dataset of multiple cycles with varying fault start points.
    """
    all_cycles = []

    # Define the range where a fault can realistically begin
    # It must start well before failure to give the AI something to predict.
    # Start: 1000 hours, End: 8000 hours (to ensure at least 2000 hours of fault progression)
    MIN_FAULT_START = 1000
    MAX_FAULT_START = TOTAL_TIME_STEPS - 2000  # Max start time is 8000 hours

    for cycle_id in range(1, num_cycles + 1):
        # Randomly choose a time step for the fault to begin
        fault_start = np.random.randint(MIN_FAULT_START, MAX_FAULT_START + 1)

        cycle_df = generate_single_pump_cycle(cycle_id, fault_start)
        all_cycles.append(cycle_df)

        # Print progress every 10 cycles
        if cycle_id % 10 == 0:
            print(f"-> Generated {cycle_id} of {num_cycles} cycles.")

    # Concatenate all cycles into one large DataFrame
    full_df = pd.concat(all_cycles)

    # Save the data
    file_path = 'pump_maintenance_data.csv'
    full_df.to_csv(file_path)

    print(f"\n--- Data Generation Complete ---")
    print(f"Total rows generated: {len(full_df)}")
    print(f"File saved to: {os.path.abspath(file_path)}")
    print(f"Columns: {full_df.columns.tolist()}")


# Execute the data generation
if __name__ == '__main__':
    generate_full_training_data()