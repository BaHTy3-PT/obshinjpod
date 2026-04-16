import pwm_dac as pwm
import signal_generator as sg
import time

# Параметры сигнала
amplitude = 3.0          # Вольт (максимальное напряжение, до ~3.3 В)
signal_frequency = 10    # Гц
sampling_frequency = 1000 # Гц (частота дискретизации)

# Настройки PWM DAC
pwm_pin = 12             # GPIO пин (BCM) для ШИМ
pwm_frequency = 500      # Частота ШИМ (Гц)
dynamic_range = 3.29     # Максимальное напряжение на выходе PWM DAC (В)

try:
    dac = pwm.PWM_DAC(pwm_pin, pwm_frequency, dynamic_range, verbose=False)
    t = 0.0
    while True:
        norm = sg.get_triangle_wave_amplitude(signal_frequency, t)
        voltage = norm * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        t += 1.0 / sampling_frequency
except KeyboardInterrupt:
    pass
finally:
    dac.deinit()
