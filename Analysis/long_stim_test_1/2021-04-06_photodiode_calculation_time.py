from sync_lib import Dataset
import matplotlib.pylab as plt
import numpy as np

path = "go_no_go_hardware_2021T12950.h5"

dset = Dataset(path)

lines = ['stim_running', 'stim_photodiode']

times_command = dset.get_rising_edges('stim_running', units='sec')
times_response = dset.get_rising_edges('stim_photodiode', units='sec')

print(times_command)
print(times_response)

plt.subplot(3, 1, 1)
plt.plot(times_response[:-2], np.diff(times_response[:-1]))
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.ylabel('Period (s)')
plt.title('Photodiode flip')

plt.subplot(3, 1, 2)
plt.plot(times_response[:-2], np.diff(times_command[:-3]))
plt.ylabel('Period (s)')
plt.title('Photodiode command')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.subplot(3, 1, 3)
plt.plot(times_response[:-1], times_response[:-1]-times_command[:-3])

plt.ylabel('Delay (s)')
plt.xlabel('Session time (seconds)')
plt.title('From Photodiode command to flip')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig('go_no_go_hardware_2021T12950_calculation_time.png')
print(times_response[0:10])
print(times_command[0:10])
