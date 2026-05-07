import time
from mcp3021_driver import MCP3021
import adc_plot

DYNAMIC_RANGE = 3.3

adc = MCP3021(DYNAMIC_RANGE)

voltage_values = []
time_values = []
duration = 3.0

try:
    start = time.time()
    while time.time() - start < duration:
        voltage = adc.get_voltage()
        elapsed = time.time() - start
        voltage_values.append(voltage)
        time_values.append(elapsed)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, DYNAMIC_RANGE)
finally:
    adc.deinit()
