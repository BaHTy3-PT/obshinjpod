import numpy as np
import time

def get_sin_wave_amplitude(freq, t):
    """
    Возвращает нормализованную амплитуду (0..1) синусоиды частотой freq (Гц) в момент t (сек).
    Формула: (sin(2πft) + 1) / 2
    """
    return (np.sin(2 * np.pi * freq * t) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    """Выжидает один период дискретизации (сек) = 1 / sampling_frequency."""
    period = 1.0 / sampling_frequency
    time.sleep(period)

https://github.com/Kabuto-Mainer/Ant-Get
