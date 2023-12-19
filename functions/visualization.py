import numpy as np
from scipy.constants import speed_of_light
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def show_signals(dat: dict, config: dict):
    """

    :param dat:
    :param config:
    :return:
    """

    t = np.linspace(0, 1 / config["modulation_frequency"], config["num_time_samples"], endpoint=False)  # time in s
    dist = 0.5 * t * speed_of_light

    plt.figure(figsize=(11, 9))
    for idx in range(config["num_components"]):
        plt.subplot(config["num_components"], 2, 2*idx+1)
        plt.plot(t*1e9, dat["sensor_demodulation_signal"][f"component{idx}"], "b-", label="sensor")
        plt.plot(t*1e9, dat["source_modulation_signal"][f"component{idx}"], "r-", label="illum.")
        plt.legend()

        if idx == 0:
            plt.title("Sensor demodulation and source modulation signals")

        if idx == config["num_components"]-1:
            plt.xlabel("Time (ns)")

        plt.subplot(config["num_components"], 2, 2*idx+2)
        plt.plot(dist, 0.5 * (dat["correlation_signal"][f"component{idx}"]+1), "k-")

        if idx == 0:
            plt.title("Correlation signals")
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
