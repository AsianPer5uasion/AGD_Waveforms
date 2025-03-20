import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from natsort import natsorted
import re

from functions import *

'''
How the reading and generation was done initially. Currently no longer relevant.
'''


#out_directory = "files/"
out_directory = "C:/Users/bowbo/Documents/LTspice/DPT/"

switching_loss = extract_measurement_data(out_directory + "DPT_AGD_IDEALISED_TEST.log", "switching_energy_loss")["v(nc_01)"]

overshoot = extract_measurement_data(out_directory + "DPT_AGD_IDEALISED_TEST.log", "overshoot")["i_max - current_reached"]
inputs_all = pd.read_csv(out_directory + "inputs.csv", header=None)
inputs_all.columns = ["Index", "A1", "T1", "A2", "T2", "A3", "T3" ,"A4","T4", "A5", "T5"]

inputs_all["Switching Loss"] = switching_loss
inputs_all["Drain Current Overshoot (A)"] = overshoot   



try:
    df = pd.read_csv("nsga_solutions_time_2.csv", encoding='latin1')  # Specify the correct encoding
except FileNotFoundError:
    print("Error: The file 'nsga_solutions_time_2.csv' does not exist.")
    df = pd.DataFrame() 

print(df)

inputs_all['ANN Overshoot'] = df['Drain Current Overshoot (A)']
inputs_all['ANN Simulated Switching Loss'] = df['Switching Loss (ÂµJ)']

inputs_all.to_csv("another_one.csv")

print(inputs_all)

fig, ax = plt.subplots()

ax.plot(inputs_all["Switching Loss"], inputs_all["Drain Current Overshoot (A)"], 'o', label='Simulated Solutions')
ax.plot(inputs_all["ANN Simulated Switching Loss"], inputs_all["ANN Overshoot"], 'o', label='NSGA-II Solutions')

ax.grid(True)

ax.set_xlabel('Switching Loss (µJ)')
ax.set_ylabel('Drain Current Overshoot (A)')
ax.legend()

plt.show()


# if not df.empty:
#     df.drop(df.columns[-1], axis=1, inplace=True)  # drop the last column

# print(len(df))

# parameterTracking = []
# plt.figure()
# for file in range(len(df)):

#     name = str(file)
#     out_array = []

#     # Charging pulse
#     time = start_time
#     out_array.append([time, 0])
#     time = time + transition_t
#     out_array.append([time, amp_upper_bound])
#     time = time + 5000
#     out_array.append([time, amp_upper_bound])
#     time = time + transition_t
#     out_array.append([time, 0])
#     time = time + 1000
#     out_array.append([time, 0])
    

#     # Start
#     fileWithInputs = [file]
#     current_file = df.iloc[file]
#     input_params = [current_file["A1"], current_file["A2"], current_file["A3"], current_file["A4"], current_file["A5"]]
 
#     for inter in range(number_of_pulses):
#         amp = input_params[inter]
#         fileWithInputs.append(amp)

#         time = time +  transition_t
#         out_array.append([time, amp])
#         time = time + length_of_pulses
#         out_array.append([time, amp])
    
#     time = time + transition_t
#     out_array.append([time, ending_level])
#     time = time + 5*length_of_pulses
#     out_array.append([time, ending_level])
#     time = time + transition_t
#     out_array.append([time, 0])

#     data = np.array(out_array)
#     time = data[:,0]
#     ampl = data[:,1]

#     plt.plot(time, ampl)
#     temp = np.array(append_suffix(out_array, "n"))

#     np.savetxt(out_directory + name, temp, fmt="%s", delimiter=" ")
#     parameterTracking.append(fileWithInputs)

# np.savetxt(out_directory + "inputs" + ".csv ", np.array(parameterTracking), delimiter=",")
# files = get_sorted_text_files(out_directory)


# plt.show()

