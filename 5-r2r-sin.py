import time
import r2r_dac
import signal_generator as sg

amplitude = 3.2
signal_freq = 10
sampling_freq = 1000
t = 0.0

try:
    dac = r2r_dac.R2R_DAC([16,20,21,25,26,17,27,22], 3.2)
    while True:
        voltage = sg.get_sin_wave_amplitude(signal_freq, t) * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_freq)
        t += 1.0 / sampling_freq
finally:
    dac.deinit()
