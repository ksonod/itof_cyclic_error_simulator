from dataclasses import dataclass, field
import numpy as np


@dataclass
class SimulationData:

    modulation_frequency: float  # Modulation frequency  Hz
    t: np.ndarray  # time data in s
    freq: np.ndarray  # frequency data in Hz
    gt_distance: np.ndarray  # Ground-truth distance in m
    gt_phase: np.ndarray  # Ground-truth phase in radian
    dist_unambiguous: float   # Unambiguous range in m
    num_components: int   # number of components
    duty_cycle: float  # duty cycle between 0 and 1
    simulated_phase: np.ndarray  # simulated phase in radian
    cyclic_error: np.ndarray  # cyclic error = Difference between simulated and GT phases
    phase_shift: list[int] = field(default_factory=list)  # phase shift in radian applied to different components
    sensor_demodulation_signal: dict = field(default_factory=dict)  # Sensor demodulation signal
    source_modulation_signal: dict = field(default_factory=dict)  # Source modulation signal (Illumination signal)
    correlation_signal: dict = field(default_factory=dict)  # Correlation of sensor and illumination signals
    fft_sensor_demodulation_signal: dict = field(default_factory=dict)  # FFT of sensor demodulation signal
    fft_source_modulation_signal: dict = field(default_factory=dict)  # FFT of source modulation signal
    fft_correlation_signal: dict = field(default_factory=dict)  # FFT of correlation signal
