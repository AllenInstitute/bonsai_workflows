import os
import numpy as np
from numpy import genfromtxt
import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt

path_draw = r"C:\Users\jeromel\Documents\Projects\Bonsai-transition\code\bonsai_workflows\Go-Nogo\drawTime.csv"

local_draw = pd.read_csv(path_draw)

local_times = local_draw['Timestamp']
local_delta = []
for index, indiv_str in enumerate(local_times):
    if index>0:
        old_time = local_time
    
    local_time = datetime.strptime(indiv_str[:-7],'%Y-%m-%dT%H:%M:%S.%f')

    if index>0:
        dt = local_time - old_time
        local_delta.append(dt.total_seconds())

plt.plot(np.cumsum(local_delta), local_delta)
plt.xlabel('Time since start(s)')
plt.ylabel('Draw period (s)')
plt.savefig('draw_time.png')
plt.show()