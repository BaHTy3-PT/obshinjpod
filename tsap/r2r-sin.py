import r2r_dac as r2r
import signal_generator as sg

amplitude = 3.2         
signal_frequency = 10  
sampling_frequency = 1000 

REF_VOLTAGE = 3.3

try:
    dac = r2r.R2R_DAC() 

    n = 0
    while True:
        t = n / sampling_frequency
        norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = amplitude * norm_amp
        value = int(round(voltage / REF_VOLTAGE * 255))
        value = max(0, min(255, value))  
        dac.set_value(value)  

        sg.wait_for_sampling_period(sampling_frequency)

        n += 1

except KeyboardInterrupt:
    pass
finally:
    if 'dac' in locals():
        dac.cleanup()
