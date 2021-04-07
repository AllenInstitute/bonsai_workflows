from sync_lib import Dataset
import matplotlib.pylab as plt
import numpy as np

path = "go_no_go_hardware_2021T12950.h5"

dset = Dataset(path)

lines = ['stim_running', 'stim_photodiode']

times = dset.get_all_times(units='sec')

end_time = 70
start_time = 60
if not end_time:
    end_time = 2**32

window = (times < end_time) & (times > start_time)

for line in lines:
    local_bit = dset._line_to_bit(line)
    print(local_bit)
    bit_trace = dset.get_bit(local_bit)
    plt.step(times[window], bit_trace[window], where='post')

plt.ylim(-0.1, 1.1)
plt.ylabel('Logic State')
plt.xlabel('time (seconds)')

plt.legend(lines)
plt.tight_layout()
plt.savefig('go_no_go_hardware_2021T12950_comparison_onset.png')

"""
plt.subplot(3, 1, 1)
plt.plot(times_bonsai_fast_sync[1:], np.diff(times_bonsai_fast_sync))
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Stimulus rendering')

plt.subplot(3, 1, 2)
plt.plot(times_bonsai_driving_photodiode[1:], np.diff(
    times_bonsai_driving_photodiode))
plt.ylabel('Period (s)')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.title('Driving photo diode signal')

plt.subplot(3, 1, 3)
plt.plot(times_photodiode[1:], np.diff(
    times_photodiode))
plt.xlabel('Time from start (s)')
plt.ylabel('Period (s)')
plt.title('Measured photo diode signal')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig('go_no_go_hardware_2021T12950_sync_lines.png')
"""
