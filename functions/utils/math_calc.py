import numpy as np

c_light_speed = 299792458  # m/s


def calculate_unambiguous_range(modulation_frequency: float) -> float:
    """
    Calculate unambiguous range. Here, the unambiguous range is the distance where phase wrapping occurs.
    :param modulation_frequency: A float expressed in Hz.
    :return: A float expressed in m.
    """
    return 0.5 * c_light_speed/modulation_frequency


def convert_rad_to_m(phase: np.ndarray, unambiguous_range: float) -> np.ndarray:
    """
    Convert phase in radian to distance in m.
    :param phase: Flattened numpy array containing phase in radian.
    :param unambiguous_range: A float for unambiguous range of iToF in m.
    :return: Distance in m (numpy array with the same dimension as the numpy array of phase)
    """
    return 0.5 * phase / np.pi * unambiguous_range

