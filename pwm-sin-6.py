import time
import pwm_dac
import signal_generator as sg

amplitude = 3.2
signal_freq = 10
sampling_freq = 1000
t = 0.0

try:
    dac = pwm_dac.PWM_DAC(12, 5000, 3.2)
    while True:
        voltage = sg.get_sin_wave_amplitude(signal_freq, t) * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_freq)
        t += 1.0 / sampling_freq
finally:
    dac.deinit()
