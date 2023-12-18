import numpy as np
from scipy import signal
from scipy.constants import speed_of_light
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def generate_signals(config: dict) -> dict:
    """
    Generate source modulation signal (illumination signal), sensor demodulation signal (local oscillator signal), and
    their correlation signal.

    :param config:
    :return:
    """

    t = np.linspace(0, 1/config["modulation_frequency"], config["num_time_samples"], endpoint=False)  # time in s
    source_mod_signal = {}  # source modulation signal
    sensor_demod_signal = {}  # sensor demodulation signal
    correlation_signal = {}  # correlation of source modulation and sensor demodulation signals.
    fft_sensor_demod_signal = {}
    fft_source_mod_signal = {}
    fft_correlation_signal = {}

    for comp_idx in range(config["num_components"]):

        # Construct sensor demodulation signal and source modulation signal.
        phi = config["phase_shift"][comp_idx]/180 * np.pi  # rad
        sensor_demod_signal[f"component{comp_idx}"] = signal.square(2 * np.pi * config["modulation_frequency"] * t)
        source_mod_signal[f"component{comp_idx}"] = 0.5 * (signal.square(2*np.pi*config["modulation_frequency"]*t-phi, duty=config["duty_cycle"])+1)


        # Get correlation in time domain by calculating inverse FFT of multiplication in frequency domain.
        fft_sensor_demod_signal[f"component{comp_idx}"] = np.fft.fft(sensor_demod_signal[f"component{comp_idx}"])
        fft_source_mod_signal[f"component{comp_idx}"] = np.fft.fft(source_mod_signal[f"component{comp_idx}"])
        fft_correlation_signal[f"component{comp_idx}"] = fft_sensor_demod_signal[f"component{comp_idx}"] * np.conj(fft_source_mod_signal[f"component{comp_idx}"])
        corr_signal = np.real(np.fft.ifft(fft_correlation_signal[f"component{comp_idx}"]))
        correlation_signal[f"component{comp_idx}"] = corr_signal/np.max(np.abs(corr_signal))

    return {
        "sensor_demodulation_signal": sensor_demod_signal,
        "source_modulation_signal": source_mod_signal,
        "correlation_signal": correlation_signal,
        "fft_sensor_demodulation_signal": fft_sensor_demod_signal,
        "fft_source_mod_signal": fft_source_mod_signal,
        "fft_correlation_signal": fft_correlation_signal
    }


def show_signals(dat: dict, config: dict):
    """

    :param dat:
    :param config:
    :return:
    """

    t = np.linspace(0, 1 / config["modulation_frequency"], config["num_time_samples"], endpoint=False)  # time in s
    dist = 0.5 * t * speed_of_light

    plt.figure(figsize=(9, 9))
    for idx in range(config["num_components"]):
        plt.subplot(config["num_components"], 2, 2*idx+1)
        plt.plot(t*1e9, dat["sensor_demodulation_signal"][f"component{idx}"], "b-", label="sensor")
        plt.plot(t*1e9, dat["source_modulation_signal"][f"component{idx}"], "r-", label="illum.")
        plt.legend()

        if idx == config["num_components"]-1:
            plt.xlabel("Time (ns)")

        plt.subplot(config["num_components"], 2, 2*idx+2)
        plt.plot(dist, 0.5 * (dat["correlation_signal"][f"component{idx}"]+1), "k-")

        if idx == config["num_components"]-1:
            plt.xlabel("Distance (m)")


def show_spectra(dat: dict, config: dict):

    t = np.linspace(0, 1 / config["modulation_frequency"], config["num_time_samples"], endpoint=False)  # time in s
    freq = np.fft.fftfreq(config["num_time_samples"], t[1] - t[0])

    fft_keys = [x for x in list(dat.keys()) if "fft" in x]

    plt.figure(figsize=(6, 8))
    for idx, fft_key in enumerate(fft_keys):
        plt.subplot(3, 1, idx+1)

        fft_signal = np.abs(dat[fft_key]["component0"])[:int(config["num_time_samples"]*0.5)]
        plt.plot(
            freq[:int(config["num_time_samples"]*0.5)]/config["modulation_frequency"],
            fft_signal/np.max(fft_signal),
            "k.-"
        )
        plt.xlim([0, 20])
        plt.annotate(text=fft_key, xy=(10, 0.9))
        plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xlabel("Harmonic order")

