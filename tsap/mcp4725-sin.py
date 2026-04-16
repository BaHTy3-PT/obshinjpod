import mcp4725_driver as mcp
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 4.5          # Вольт 5
signal_frequency = 10    # Гц
sampling_frequency = 1000 # Гц

# Настройки MCP4725
dynamic_range = 5.0      
i2c_address = 0x61       

try:
    
    dac = mcp.MCP4725(dynamic_range, i2c_address, verbose=False)
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
