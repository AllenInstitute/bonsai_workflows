from sync_lib import Dataset
import matplotlib.pylab as plt
import numpy as np

path = "go_no_go_hardware_2021T12950.h5"

dset = Dataset(path)

# This is the fastest output from bonsai to digital line
times_bonsai_fast_sync = dset.get_rising_edges('vsync_stim', units='sec')

# This is the driving signal behind the photodiode
times_bonsai_driving_photodiode = dset.get_rising_edges(
    'stim_running', units='sec')

times_photodiode = dset.get_rising_edges('stim_photodiode', units='sec')

plt.subplot(3, 1, 1)
plt.plot(times_bonsai_fast_sync[1:], np.diff(times_bonsai_fast_sync))
plt.ylim(0.02, 0.04)
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Stimulus rendering')

plt.subplot(3, 1, 2)
plt.plot(times_bonsai_driving_photodiode[1:], np.diff(
    times_bonsai_driving_photodiode))
plt.ylim(0.995, 1.005)
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Driving photo diode signal')

plt.subplot(3, 1, 3)
plt.plot(times_photodiode[1:], np.diff(
    times_photodiode))
plt.ylim(0.995, 1.005)
plt.xlabel('Time from start (s)')
plt.ylabel('Period (s)')
plt.title('Measured photo diode signal')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig('go_no_go_hardware_2021T12950_sync_lines_zoomed.png')
