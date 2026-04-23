import r2r_dac as r2r
import signal_generator as sg
import time

def main():
    amplitude = 3.2          
    signal_frequency = 10   
    sampling_frequency = 1000  

    dac = None
    try:

        dac = r2r.R2RDAC()
        start_time = time.time()
        while True:
        
            t = time.time() - start_time
        
            norm_amp = sg.get_sin_wave_amplitude(signal_frequency, t)

            voltage = norm_amp * amplitude

            dac.set_voltage(voltage)
            
            sg.wait_for_sampling_period(sampling_frequency)
    except KeyboardInterrupt:
        print("\nГенерация остановлена пользователем")
    finally:
        if dac:
            dac.deinit()

if __name__ == "__main__":
    main()
