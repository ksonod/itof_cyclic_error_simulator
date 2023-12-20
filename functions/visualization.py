import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from enum import Enum
from data_model.simulation_data import SimulationData
from functions.utils.math_calc import convert_rad_to_m

class DepthUnit(Enum):
    METER = "Distance (m)"
    CENTIMETER = "Distance (cm)"
    RADIAN = "Phase (rad.)"
    DEGREE = "Phase (deg.)"


class DataVisualizer:
    def __init__(self, figure_config: dict, dat: SimulationData):
        self.figure_config = figure_config
        self.dat = dat

    def __call__(self):
        if self.figure_config["show_signals"]:
            self.show_signals(self.dat, self.figure_config)
        if self.figure_config["show_spectra"]:
            self.show_spectra(self.dat)
        if self.figure_config["show_phase_signals_and_cyclic_error"]:
            self.show_phase_signals_and_cyclic_error(self.dat, self.figure_config)

    @staticmethod
    def show_signals(dat: SimulationData, figure_config):
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

            x_data = dat.gt_phase

            if "unit" in figure_config:
                if figure_config["unit"] == DepthUnit.RADIAN:
                    pass  # No modification is needed.
                elif figure_config["unit"] == DepthUnit.DEGREE:  # in degree
                    x_data = np.rad2deg(dat.gt_phase)
                elif figure_config["unit"] == DepthUnit.METER:  # in m
                    x_data = dat.gt_distance
                elif figure_config["unit"] == DepthUnit.CENTIMETER:  # in cm
                    x_data = dat.gt_distance * 100
                else:
                    raise NotImplementedError("Select a right unit.")

            plt.plot(x_data, 0.5 * (dat.correlation_signal[f"component{idx}"]+1), "k-")

            if idx == 0:
                plt.title("Correlation signals")
            if idx == dat.num_components-1:
                plt.xlabel(figure_config["unit"].value)

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
    def show_phase_signals_and_cyclic_error(dat: SimulationData, figure_config):

        x_gt_data = dat.gt_phase
        y_simulated_data = dat.simulated_phase
        y_cyclic_error_data = dat.cyclic_error
        y_fft_cyclic_error_data = np.abs(dat.fft_cyclic_error[:int(np.round(0.5*dat.t.shape[0]))])
        y_fft_cyclic_error_data /= np.max(y_fft_cyclic_error_data)

        if "unit" in figure_config:
            if figure_config["unit"] == DepthUnit.RADIAN:
                pass  # No modification is needed.
            elif figure_config["unit"] == DepthUnit.DEGREE:
                x_gt_data *= 180/np.pi
                y_simulated_data *= 180/np.pi
                y_cyclic_error_data *= 180/np.pi
            elif figure_config["unit"] == DepthUnit.METER:
                x_gt_data = dat.gt_distance
                y_simulated_data = convert_rad_to_m(dat.simulated_phase, dat.dist_unambiguous)
                y_cyclic_error_data = convert_rad_to_m(dat.cyclic_error, dat.dist_unambiguous)
            elif figure_config["unit"] == DepthUnit.CENTIMETER:
                x_gt_data = dat.gt_distance
                y_simulated_data = convert_rad_to_m(dat.simulated_phase, dat.dist_unambiguous) * 100
                y_cyclic_error_data = convert_rad_to_m(dat.cyclic_error, dat.dist_unambiguous) * 100
            else:
                raise NotImplementedError("Select a right unit.")

        # y label creation for showing cyclic error.
        ylabel = figure_config["unit"].value.split(" ")
        ylabel.insert(1, "error")
        ylabel = " ".join(ylabel)

        plt.figure(figsize=(15, 4))
        plt.subplot(131)
        plt.plot(x_gt_data, x_gt_data, "k--", label="GT")
        plt.plot(x_gt_data, y_simulated_data, "r-", label="Simulation")
        plt.xlabel("Ground-truth " + figure_config["unit"].value.lower())
        plt.ylabel(figure_config["unit"].value)
        plt.legend()

        plt.subplot(132)
        plt.plot(x_gt_data, y_cyclic_error_data, "k-")
        plt.xlabel("Ground-truth " + figure_config["unit"].value.lower())
        plt.ylabel(ylabel)

        plt.subplot(133)
        plt.plot(
            dat.freq[:int(np.round(0.5*dat.t.shape[0]))]/dat.modulation_frequency,
            y_fft_cyclic_error_data,
            "k.-"
        )
        plt.xlabel("Harmonic order")
        plt.xlim([0, 30])
        plt.ylabel(ylabel)
        plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        plt.tight_layout()
