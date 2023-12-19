import numpy as np
from scipy import signal
from data_model.simulation_data import SimulationData


class PhaseSimulator:
    """
    With PhaseSimulator, sensor demodulation signal, source modulation signal, and their correlation signal can be
    calculated. Using these values, phase is computed. The computed phase is compared with ground-truth phase in order
    to evaluate phase error.
    """

    def __init__(self, config: dict):
        self.simulation_data = None
        self.speed_of_light = 299792458  # m/s
        self.config = config  # config dict

    def __call__(self):
        self.prepare_basic_simulation_data()
        self.generate_signals()
        self.calculate_phase_and_cyclic_error()
        return self.simulation_data

    def prepare_basic_simulation_data(self):
        """
        Prepare basic data for further simulation.
        """

        if "phase_shift" in self.config:
            phase_shift = np.deg2rad(self.config["phase_shift"])
        else:
            phase_shift = self.config["num_components"] * [0]

        if "duty_cycle" in self.config:
            duty_cycle = self.config["duty_cycle"]
        else:
            duty_cycle = 0.0

        if "source_modulation_signal_phase_offset" in self.config:
            source_modulation_signal_phase_offset = np.deg2rad(
                self.config["source_modulation_signal_phase_offset"]
            )  # in rad
        else:
            source_modulation_signal_phase_offset = 0.0

        t = np.linspace(
            0, 1/self.config["modulation_frequency"], self.config["num_time_samples"],
            endpoint=False
        )  # time in s
        dist = 0.5 * t * self.speed_of_light  # distance in m
        dist_unambiguous = 0.5 * self.speed_of_light / self.config["modulation_frequency"]  # unambiguous range
        gt_phase = dist / dist_unambiguous * 2 * np.pi  # Ground truth phase

        # Save all basic simulation data
        self.simulation_data = SimulationData(
            modulation_frequency=self.config["modulation_frequency"],
            t=t,
            freq=np.fft.fftfreq(self.config["num_time_samples"], t[1] - t[0]),
            gt_distance=dist,
            gt_phase=gt_phase,
            dist_unambiguous=dist_unambiguous,
            num_components=self.config["num_components"],
            phase_shift=phase_shift,
            source_modulation_signal_phase_offset=source_modulation_signal_phase_offset,
            duty_cycle=duty_cycle,
            simulated_phase=np.zeros_like(t),
            cyclic_error=np.zeros_like(t)
        )

    def generate_signals(self):
        """
        Generate source modulation signal (illumination signal), sensor demodulation signal (local oscillator signal),
        and their correlation signal.
        """

        for comp_idx in range(self.simulation_data.num_components):

            # Step1: Construct sensor demodulation signal and source modulation signal.
            phi = self.simulation_data.phase_shift[comp_idx]  # rad

            self.simulation_data.sensor_demodulation_signal[f"component{comp_idx}"] = signal.square(
                2 * np.pi * self.simulation_data.modulation_frequency * self.simulation_data.t
            )

            self.simulation_data.source_modulation_signal[f"component{comp_idx}"] = 0.5 * (
                    signal.square(
                        2 * np.pi * self.simulation_data.modulation_frequency * self.simulation_data.t - phi - self.simulation_data.source_modulation_signal_phase_offset,
                        duty=self.simulation_data.duty_cycle
                    ) + 1
            )

            # Step2: Get correlation in time domain by calculating inverse FFT of multiplication in frequency domain.
            self.simulation_data.fft_sensor_demodulation_signal[f"component{comp_idx}"] = np.fft.fft(
                self.simulation_data.sensor_demodulation_signal[f"component{comp_idx}"]
            )

            self.simulation_data.fft_source_modulation_signal[f"component{comp_idx}"] = np.fft.fft(
                self.simulation_data.source_modulation_signal[f"component{comp_idx}"]
            )

            self.simulation_data.fft_correlation_signal[f"component{comp_idx}"] = \
                self.simulation_data.fft_sensor_demodulation_signal[f"component{comp_idx}"] * \
                np.conj(self.simulation_data.fft_source_modulation_signal[f"component{comp_idx}"])

            corr_signal = np.real(
                np.fft.ifft(
                    self.simulation_data.fft_correlation_signal[f"component{comp_idx}"]
                )
            )
            self.simulation_data.correlation_signal[f"component{comp_idx}"] = corr_signal/np.max(np.abs(corr_signal))
        return 0

    def calculate_phase_and_cyclic_error(self):
        """
        Calculate phase and cyclic error (a.k.a. wiggling error)
        """
        simulated_phase = []

        for time_idx in range(self.simulation_data.t.shape[0]):
            sampled_corr_signal = []
            for comp_idx in range(self.simulation_data.num_components):
                sampled_corr_signal.append(self.simulation_data.correlation_signal[f"component{comp_idx}"][time_idx])

            sampled_corr_signal = np.array(sampled_corr_signal)
            fft_sampled_corr_signal = np.fft.fft(sampled_corr_signal)
            simulated_phase.append(np.angle(fft_sampled_corr_signal)[1])

        simulated_phase = np.array(simulated_phase)

        # Correct phase wrapping effect
        simulated_phase = np.unwrap(np.mod(simulated_phase, 2 * np.pi), period=2*np.pi)
        cyclic_error = simulated_phase - self.simulation_data.gt_phase
        center_ce = np.mean(cyclic_error)
        cyclic_error -= center_ce
        simulated_phase -= center_ce

        # Store simulated data
        self.simulation_data.cyclic_error = cyclic_error
        self.simulation_data.simulated_phase = simulated_phase
        self.simulation_data.rms_phase_error = np.sqrt(np.mean(cyclic_error**2))
