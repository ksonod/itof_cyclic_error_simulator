import numpy as np
from scipy import signal
from data_model.simulation_data import SimulationData


class PhaseSimulator:
    def __init__(self, config):
        self.simulation_data = None
        self.speed_of_light = 299792458  # m/s
        self.config = config

    def __call__(self):
        self.prepare_basic_simulation_data()
        self.generate_signals()
        self.calculate_phase_and_cyclic_error()
        return self.simulation_data

    def prepare_basic_simulation_data(self):

        if "phase_shift" in self.config:
            phase_shift = self.config["phase_shift"]
        else:
            phase_shift = self.config["num_components"] * [0]

        if "duty_cycle" in self.config:
            duty_cycle = self.config["duty_cycle"]
        else:
            duty_cycle = 0.0

        t = np.linspace(
            0, 1/self.config["modulation_frequency"], self.config["num_time_samples"],
            endpoint=False
        )  # time in s
        dist = 0.5 * t * self.speed_of_light  # distance in m
        dist_unambiguous = 0.5 * self.speed_of_light / self.config["modulation_frequency"]  # unambiguous range
        gt_phase = dist / dist_unambiguous * 2 * np.pi  # Ground truth phase

        self.simulation_data = SimulationData(
            modulation_frequency=self.config["modulation_frequency"],
            t=t,
            freq=np.fft.fftfreq(self.config["num_time_samples"], t[1] - t[0]),
            gt_distance=dist,
            gt_phase=gt_phase,
            dist_unambiguous=dist_unambiguous,
            num_components=self.config["num_components"],
            phase_shift=phase_shift,
            duty_cycle=duty_cycle,
            simulated_phase=np.zeros_like(t),
            cyclic_error=np.zeros_like(t)
        )

    def generate_signals(self):
        """
        Generate source modulation signal (illumination signal), sensor demodulation signal (local oscillator signal), and
        their correlation signal.

        :param config:
        """

        source_mod_signal = {}  # source modulation signal
        sensor_demod_signal = {}  # sensor demodulation signal
        correlation_signal = {}  # correlation of source modulation and sensor demodulation signals.
        fft_sensor_demod_signal = {}
        fft_source_mod_signal = {}
        fft_correlation_signal = {}

        for comp_idx in range(self.simulation_data.num_components):

            # Construct sensor demodulation signal and source modulation signal.
            phi = self.simulation_data.phase_shift[comp_idx]/180 * np.pi  # rad
            sensor_demod_signal[f"component{comp_idx}"] = signal.square(2 * np.pi * self.simulation_data.modulation_frequency * self.simulation_data.t)
            source_mod_signal[f"component{comp_idx}"] = 0.5 * (
                    signal.square(
                        2 * np.pi * self.simulation_data.modulation_frequency * self.simulation_data.t-phi,
                        duty=self.simulation_data.duty_cycle
                    ) + 1
            )


            # Get correlation in time domain by calculating inverse FFT of multiplication in frequency domain.
            fft_sensor_demod_signal[f"component{comp_idx}"] = np.fft.fft(
                sensor_demod_signal[f"component{comp_idx}"]
            )
            fft_source_mod_signal[f"component{comp_idx}"] = np.fft.fft(
                source_mod_signal[f"component{comp_idx}"]
            )
            fft_correlation_signal[f"component{comp_idx}"] = fft_sensor_demod_signal[f"component{comp_idx}"] * np.conj(fft_source_mod_signal[f"component{comp_idx}"])
            corr_signal = np.real(
                np.fft.ifft(
                    fft_correlation_signal[f"component{comp_idx}"]
                )
            )
            correlation_signal[f"component{comp_idx}"] = corr_signal/np.max(np.abs(corr_signal))

        self.simulation_data.sensor_demodulation_signal = sensor_demod_signal
        self.simulation_data.source_modulation_signal = source_mod_signal
        self.simulation_data.correlation_signal = correlation_signal
        self.simulation_data.fft_sensor_demodulation_signal = fft_sensor_demod_signal
        self.simulation_data.fft_source_mod_signal = fft_source_mod_signal
        self.simulation_data.fft_correlation_signal = fft_correlation_signal

    def calculate_phase_and_cyclic_error(self):
        simulated_phase = []

        for time_idx in range(self.simulation_data.t.shape[0]):
            sampled_corr_signal = []
            for comp_idx in range(self.simulation_data.num_components):
                sampled_corr_signal.append(self.simulation_data.correlation_signal[f"component{comp_idx}"][time_idx])

            sampled_corr_signal = np.array(sampled_corr_signal)
            fft_sampled_corr_signal = np.fft.fft(sampled_corr_signal)
            simulated_phase.append(np.angle(fft_sampled_corr_signal)[1])

        simulated_phase = np.array(simulated_phase)
        simulated_phase = np.unwrap(np.mod(simulated_phase, 2 * np.pi), period=2*np.pi)

        if np.sum(simulated_phase > 2*np.pi) != 0:  # If most phase data are above 2pi because of unwrapping, 2pi is subtracted.
            simulated_phase -= 2 * np.pi

        self.simulation_data.cyclic_error = simulated_phase-self.simulation_data.gt_phase
        self.simulation_data.simulated_phase = simulated_phase
