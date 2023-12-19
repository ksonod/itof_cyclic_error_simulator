import numpy as np
from scipy import signal


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

