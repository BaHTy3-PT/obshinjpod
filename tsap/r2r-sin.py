import r2r_dac as r2r
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

# Пины R2R-ЦАП (BCM, от младшего бита к старшему)
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]
dynamic_range = 3.183

try:
    dac = r2r.R2R_DAC(dac_bits, dynamic_range, verbose=False)
    t = 0.0
    while True:
        norm = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = norm * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        t += 1.0 / sampling_frequency
except KeyboardInterrupt:
    pass
finally:
    dac.deinit()
