import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from data_model.simulation_data import SimulationData


class DataVisualizer:
    def __init__(self, figure_config: dict, dat: SimulationData):
        self.figure_config = figure_config
        self.dat = dat

    def __call__(self):
        if self.figure_config["show_signals"]:
            self.show_signals(self.dat)
        if self.figure_config["show_spectra"]:
            self.show_spectra(self.dat)
        if self.figure_config["show_phase_signals_and_cyclic_error"]:
            self.show_phase_signals_and_cyclic_error(self.dat)

    @staticmethod
    def show_signals(dat: SimulationData):
        """
        Show sensor and illumination signals
        :param dat: SimulationData
        """

        plt.figure(figsize=(11, 9))
        for idx in range(dat.num_components):
            plt.subplot(dat.num_components, 2, 2*idx+1)
            plt.plot(dat.t*1e9, dat.sensor_demodulation_signal[f"component{idx}"], "b-", label="sensor")
            plt.plot(dat.t*1e9, dat.source_modulation_signal[f"component{idx}"], "r-", label="illum.")
            plt.legend()

            if idx == 0:
                plt.title("Sensor and illumination signals")

            if idx == dat.num_components-1:  # Last
                plt.xlabel("Time (ns)")

            plt.subplot(dat.num_components, 2, 2*idx+2)
            plt.plot(dat.gt_distance, 0.5 * (dat.correlation_signal[f"component{idx}"]+1), "k-")

            if idx == 0:
                plt.title("Correlation signals")
            if idx == dat.num_components-1:
                plt.xlabel("Distance (m)")

    @staticmethod
    def show_spectra(dat: SimulationData):
        """
        Visualize FT Spectra.
        :param dat:  SimulationData
        """

        dat_stock = [
            dat.fft_sensor_demodulation_signal,
            dat.fft_source_modulation_signal,
            dat.fft_correlation_signal
        ]

        label = [
            "Sensor",
            "Illumination",
            "Correlation"
        ]

        plt.figure(figsize=(6, 8))
        for idx, fft_dat in enumerate(dat_stock):
            plt.subplot(3, 1, idx+1)

            fft_signal = np.abs(fft_dat["component0"])[:int(np.round(dat.t.shape[0]*0.5))]
            plt.plot(
                dat.freq[:int(np.round(dat.t.shape[0]*0.5))] / dat.modulation_frequency,
                fft_signal/np.max(fft_signal),
                "k.-"
            )
            plt.xlim([0, 20])
            plt.annotate(text=label[idx], xy=(15, 0.9))
            plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xlabel("Harmonic order")

    @staticmethod
    def show_phase_signals_and_cyclic_error(dat: SimulationData):

        plt.figure(figsize=(12,4))
        plt.subplot(121)
        plt.plot(dat.gt_phase, dat.gt_phase, "k--", label="GT")
        plt.plot(dat.gt_phase, dat.simulated_phase, "r-", label="Simulated phase")
        plt.xlabel("Ground-truth phase (rad.)")
        plt.ylabel("Phase (rad.)")
        plt.legend()

        plt.subplot(122)
        plt.plot(dat.gt_phase, dat.cyclic_error, "k-")
        plt.xlabel("Ground-truth phase (rad.)")
        plt.ylabel("Phase error (rad.)")
