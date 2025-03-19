import random
import numpy as np
import matplotlib.pyplot as plt
import os
from natsort import natsorted

amp_upper_bound = 10 
amp_lower_bound = 0
number_of_pulses = 5
length_of_pulses = 12 #n
ending_level = 10

number_of_variations = 2
start_time = 180000 #n
transition_t = 1 #n


#out_directory = "files/"
out_directory = "C:/Users/bowbo/Documents/LTspice/DPT/"


def get_sorted_text_files(directory):
    try:
        # Get all files in the directory
        files = os.listdir(directory)
        
        # Filter for files that end with .txt
        text_files = [file for file in files if file.endswith('.txt')]
        
        # Apply natural sorting
        sorted_text_files = natsorted(text_files)
        
        return sorted_text_files
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def append_suffix(array, suffix):
    for row in array:
        if len(row) > 0:  # Ensure the row is not empty
            row[0] = str(row[0]) + suffix
    return array


parameterTracking = []
plt.figure()
for file in range(number_of_variations):

    name = str(file)
    out_array = []

    # Charging pulse
    timeOther = start_time
    out_array.append([timeOther, 0])
    timeOther = timeOther + transition_t
    out_array.append([timeOther, amp_upper_bound])
    timeOther = timeOther + 5000
    out_array.append([timeOther, amp_upper_bound])
    timeOther = timeOther + transition_t
    out_array.append([timeOther, 0])
    timeOther = timeOther + 1000
    out_array.append([timeOther, 0])
    

    # Start
    time_count = timeOther
    fileWithInputs = [file]
    optimal = [0.056867,	1.75759,	9.790786,	5.850278,	6.234675]
    worst = [9.681817,	9.715738,	1.077484,	0.062088,	0.794181]

    temp = []
    if file == 0:
        temp = optimal
    else:
        temp = worst

    for inter in range(number_of_pulses):
        amp = temp[inter]
        fileWithInputs.append(amp)

        time_count = time_count +  transition_t 
        out_array.append([time_count, amp])
        time_count = time_count + length_of_pulses
        out_array.append([time_count, amp])
    
    time_count = time_count + transition_t
    out_array.append([time_count, ending_level])
    time_count = time_count + 5*length_of_pulses
    out_array.append([time_count, ending_level])
    time_count = time_count + transition_t
    out_array.append([time_count, 0])

    data = np.array(out_array)
    time = data[:,0]
    ampl = data[:,1]

    plt.plot(time, ampl)
    temp = np.array(append_suffix(out_array, "n"))

    np.savetxt(out_directory + name, temp, fmt="%s", delimiter=" ")
    parameterTracking.append(fileWithInputs)

np.savetxt(out_directory + "inputs" + ".csv ", np.array(parameterTracking), delimiter=",")
files = get_sorted_text_files(out_directory)


plt.show()

