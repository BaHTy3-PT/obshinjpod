import time
import mcp4725_driver_4
import signal_generator as sg

amplitude = 5.0
signal_freq = 10
sampling_freq = 200
t = 0.0

try:
    dac = mcp4725_driver.MCP4725(5.0, address=0x61)
    while True:
        voltage = sg.get_sin_wave_amplitude(signal_freq, t) * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_freq)
        t += 1.0 / sampling_freq
finally:
    dac.deinit()
