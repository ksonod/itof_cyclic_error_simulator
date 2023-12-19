from dataclasses import dataclass, field
import numpy as np

@dataclass
class SimulationData:

    modulation_frequency: float
    t: np.ndarray  # time data
    freq: np.ndarray  # frequency data
    gt_distance: np.ndarray  # Ground-truth distance
    gt_phase: np.ndarray  # Ground-truth phase
    dist_unambiguous: float   # Unambiguous range
    num_components: int   # number of components
    duty_cycle: float  # duty cycle
    simulated_phase: np.ndarray
    cyclic_error: np.ndarray

    sensor_demodulation_signal: dict = field(default_factory=dict)
    source_modulation_signal: dict = field(default_factory=dict)
    correlation_signal: dict = field(default_factory=dict)
    fft_sensor_demodulation_signal: dict = field(default_factory=dict)
    fft_source_mod_signal: dict = field(default_factory=dict)
    fft_correlation_signal: dict = field(default_factory=dict)
    phase_shift: list[int] = field(default_factory=list)  # phase shift
