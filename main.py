from functions.signal import *
from functions.visualization import *

CONFIG = {
    "num_components": 4,
    "phase_shift": [0, 90, 180, 270],  # in degree
    "modulation_frequency": 20e6,  # Hz
    "duty_cycle": 0.5,
    "num_time_samples": 3000
}


def run_simulation(config):

    dat = generate_signals(config)
    show_signals(dat, config)
    show_spectra(dat, config)
    phase_signal = calculate_phase_and_cyclic_error(dat, config)
    show_phase_signals_and_cyclic_error(phase_signal)
    plt.show()


if __name__ == "__main__":
    run_simulation(config=CONFIG)
