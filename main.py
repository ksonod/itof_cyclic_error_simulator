from functions.signal import *
from functions.visualization import *

CONFIG = {
    "num_components": 4,
    "phase_shift": [0, 90, 180, 270],  # in degree
    "modulation_frequency": 20e6,  # Hz
    "duty_cycle": 0.5,
    "num_time_samples": 3000,
    "figure": {
        "show_signals": True,
        "show_spectra": True,
        "show_phase_signals_and_cyclic_error": True
    }
}


def run_simulation(config):

    phase_simulator = PhaseSimulator(config)
    simulation_data = phase_simulator()

    data_visualizer = DataVisualizer(config["figure"], simulation_data)
    data_visualizer()

    plt.show()


if __name__ == "__main__":
    run_simulation(config=CONFIG)
