import matplotlib.pyplot as plt
import random
import numpy as np

from functions import *

amp_upper_bound = 10
amp_lower_bound = 0
ampFactor = 1 #7E-3

number_of_pulses = 5
length_of_pulses = 12 #n
ending_level = amp_upper_bound * ampFactor

pulse_duration_lower_bound = 1
pulse_duration_upper_bound = 18

number_of_variations = 3000
start_time = 180000 #n
transition_t = 1 #n

total_desired_main_pulse_duration = (12*5)*2 #n

#out_directory = "files/"
out_directory = "C:/Users/bowbo/Documents/LTspice/DPT/"
#out_directory = "filesTrial/"

def CreateSimFiles(directory):
    df = pd.read_csv(directory)

    parameterTracking = []
    time_of_modulated_pulses = 0

    number_of_variations = len(df)

    for file in range(number_of_variations):

        name = str(file)
        out_array = []

        # Charging pulse
        time = start_time
        out_array.append([time, 0])
        time = time + transition_t
        out_array.append([time, amp_upper_bound * ampFactor])
        time = time + 5000
        out_array.append([time, amp_upper_bound * ampFactor])
        time = time + transition_t
        out_array.append([time, 0])
        time = time + 1000
        out_array.append([time, 0])
        
        time_of_modulated_pulses = time

        # Start
        fileWithInputs = [file]
        input_params = [df["A1"][file], df["A2"][file], df["A3"][file], df["A4"][file], df["A5"][file]]
        input_params = [element * ampFactor for element in input_params]
        input_params_time = [df["T1"][file], df["T2"][file], df["T3"][file], df["T4"][file], df["T5"][file]]
    
        for inter in range(len(input_params)):

            # Sort out the logging of the time parameters 
            amp = input_params[inter]
            t = input_params_time[inter]
            fileWithInputs.append(amp)
            time = time +  transition_t
            out_array.append([time, amp])
            time = time + input_params_time[inter]
            fileWithInputs.append(t)
            out_array.append([time, amp])
        
        time = time + transition_t
        out_array.append([time, ending_level])
        time = time + (total_desired_main_pulse_duration - (time - time_of_modulated_pulses))
        out_array.append([time, ending_level])
        time = time + transition_t
        out_array.append([time, 0])

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

CreateSimFiles("nsga_solutions_time_3.csv")