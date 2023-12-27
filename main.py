from functions.signal import PhaseSimulator
from functions.visualization import DepthUnit, DataVisualizer
import matplotlib.pyplot as plt

CONFIG = {
    "num_components": 4,  # Number of components
    "phase_shift": [0, 90, 180, 270],  # in degree
    "modulation_frequency": 20e6,  # Hz
    "duty_cycle": 0.5,  # Duty cycle between 0 and 1
    "num_time_samples": 3000,  # Number of samples in time domain.
    # "source_modulation_signal_phase_offset": 45,  # in degree
    "figure": {  # Figure config
        "show_signals": True,
        "show_spectra": True,
        "show_phase_signals_and_cyclic_error": True,
        "unit": DepthUnit.RADIAN
    }
}


def run_simulation(config: dict):

    phase_simulator = PhaseSimulator(config)
    simulation_data = phase_simulator()

    data_visualizer = DataVisualizer(config["figure"], simulation_data)
    data_visualizer()

    plt.show()


if __name__ == "__main__":
    run_simulation(config=CONFIG)
