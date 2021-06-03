from sync_lib import Dataset
import matplotlib.pylab as plt
import numpy as np
from numpy import genfromtxt
import pandas as pd

path = "go_no_go_hardware_2021T155621.h5"
lick_time = "lick_times.csv"
my_data = pd.read_csv(lick_time)
my_data['Timestamp'] = pd.to_datetime(my_data['Timestamp'])
list_delta = (my_data['Timestamp'] - my_data['Timestamp'][0]).dt
my_data['Difference'] = (list_delta.microseconds +
                         list_delta.seconds * 10**6) / 10**6
print(my_data['Difference'])

dset = Dataset(path)

# This is the fastest output from bonsai to digital line
times_bonsai_fast_sync = dset.get_rising_edges('vsync_stim', units='sec')

# This is the driving signal behind the photodiode
times_bonsai_driving_photodiode = dset.get_rising_edges(
    'stim_running', units='sec')

times_photodiode = dset.get_rising_edges('stim_photodiode', units='sec')

ax1 = plt.subplot(4, 1, 1)
plt.plot(times_bonsai_fast_sync[1:], np.diff(times_bonsai_fast_sync))
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Stimulus rendering')
#plt.ylim(0.03, 0.04)

plt.subplot(4, 1, 2, sharex=ax1)
plt.plot(times_bonsai_driving_photodiode[1:], np.diff(
    times_bonsai_driving_photodiode))
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Driving photo diode signal')
#plt.ylim(0.999, 1.001)

plt.subplot(4, 1, 3, sharex=ax1)
plt.plot(times_photodiode[1:], np.diff(
    times_photodiode))
plt.xlabel('Time from start (s)')
plt.ylabel('Period (s)')
plt.title('Measured photo diode signal')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
#plt.ylim(0.9999, 1.0001)
plt.xlim(15, 320)

plt.subplot(4, 1, 4)
times_licks = np.array(my_data['Difference'])
plt.plot(times_licks, np.ones(times_licks.shape), 'r.')
plt.xlabel('Time from first keypress (s)')
plt.ylabel('Is key pressed?')
plt.title('Manual key press')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.tight_layout()
plt.savefig('go_no_go_hardware_2021T155621_sync_lines.png')
