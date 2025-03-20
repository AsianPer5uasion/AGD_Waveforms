import matplotlib.pyplot as plt
import random
import numpy as np
import os

from functions import *
from config import *


def currentFromPMOS(PMOS):
    return 0.0899*PMOS # Returns in amps

def pre_pulse(time_domain = True):

    '''
    Returns the first pulse of the waveform.
    '''

    out_arr = []
    if time_domain:
        t_c = START_TIME_OFFSET
        out_arr.append([0, t_c])

        t_c = t_c + TRANSITION_TIME
        out_arr.append([FIRST_PULSE_AMP, t_c])

        t_c = t_c + FIRST_PULSE_DURATION
        out_arr.append([FIRST_PULSE_AMP, t_c])

        t_c = t_c + TRANSITION_TIME
        out_arr.append([-1*FIRST_PULSE_AMP, t_c])

        t_c = t_c + FIRST_PULSE_DURATION
        out_arr.append([-1*FIRST_PULSE_AMP, t_c])

        t_c = t_c + TRANSITION_TIME
        out_arr.append([0, t_c])

        t_c = t_c + OFF_TIME
        out_arr.append([0, t_c])

    else:
        # implement "step" domain?
        pass

    return out_arr
    

def genWave():

    '''
    Generates the "step-domain" waveform that corresponds to the AGD parameters.'''

    q_t = int(Q_T * random.uniform(1.0 - VAR_PERCENTAGE, 1 + VAR_PERCENTAGE))
    q_gd = q_t * (Q_GD/Q_T)
    q_gs1 = q_t * (Q_GS1/Q_T)
    q_r = q_t - q_gd - q_gs1

    #print("Charges: ", q_t, q_gd, q_gs1, q_r)

    out_arr = []

    # Pulse 1 -> High 
    a1 = random.randint(1,PMOS_NUMBER)
    t1 = int((q_gs1/currentFromPMOS(a1)) * 0.5)
    out_arr.append([a1, 0 + t1])
 
    # Pulse 2 -> Low
    a2 = random.randint(1,a1)
    t2 = int((q_gd/currentFromPMOS(a2)) * 0.5)
    out_arr.append([a2, t1 + t2])
    
    # Pulse 2 -> High
    a3 = random.randint(a2,PMOS_NUMBER)
    t3 = int((q_r/currentFromPMOS(a3)) * 0.5)
    out_arr.append([a3, t1 + t2 + t3])
    
    # x, y = zip(*out_arr)
    # print("Time: " + str(y))
    # print("Amp: " + str(x))
    
    return out_arr

def to_time_domain(arr, plot = False):
    '''
    Converts the "step-domain" waveform to a time-domain waveform that the sim can use.
    '''

    a_t, t_t = zip(*arr)
   
    a_t = [currentFromPMOS(a_t[a_n]) for a_n in range(len(a_t))]
    t_t = [2*t_t[t_n] for t_n in range(len(t_t))]

    out_arr = []
    out_arr.append([0, 0])
    out_arr.append([a_t[0], 0 + TRANSITION_TIME])
    out_arr.append([a_t[0], t_t[0]])
    out_arr.append([a_t[1], t_t[0] + TRANSITION_TIME])
    out_arr.append([a_t[1], t_t[1]])
    out_arr.append([a_t[2], t_t[1] + TRANSITION_TIME])
    out_arr.append([a_t[2], t_t[2]])

    x, y = zip(*out_arr)
    
    plt.ioff
    if plot:
        plt.ion()
        fig, ax = plt.subplots();
        ax.plot(y, x, 'o-');
        ax.set(xlabel='time (ns)', ylabel='current (A)');
        ax.set_ylim(0, np.max(x) + 0.5);
        fig.show();
        ax.grid();

    # print(out_arr)
    # print("Time: " + str(y))
    # print("Amp: " + str(x))
    return out_arr

def append_suffix(array, suffix):
    array = array.tolist()
    for row in array:
        if len(row) > 0:  # Ensure the row is not empty
             row[1] = str(row[1]) + suffix
    return array


def writeForLTspice(arr, name,plot = False, write = True, writeToDPT = False, out_d = OUT_DIR):
    # Input time-domain list

    '''
    Top-level function that generates and writes the waveforms to fileLocation.
    '''
    x, y = zip(*arr)
    y = [y[x] + pre_pulse()[-1][1] for x in range(len(y))]
    arr = list(zip(x, y))
 
    out_arr = np.concatenate((pre_pulse(),np.array(arr)), axis=0)
    x, y = zip(*out_arr)

    plt.ioff()
    if plot:
        
        plt.ion()
        fig, ax = plt.subplots();
        ax.plot(y, x, 'o-');
        ax.set(xlabel='time (ns)', ylabel='current (A)');
        ax.set_ylim(-0.2, np.max(x) + 0.5);
        fig.show();
        ax.grid();

    out_arr = append_suffix(out_arr, "n")
    out_arr = [[p, q] for q, p in out_arr]



    if write:
        os.makedirs(out_d, exist_ok=True)
        np.savetxt(out_d + "/" +name, out_arr, fmt="%s", delimiter=" ")

    if writeToDPT:
        np.savetxt(DPT_OUT_DIR + name, out_arr, fmt="%s", delimiter=" ")

    return list(zip(x, y))


def plotA(arr, label: str = None,fig_ax=None):
    if fig_ax is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = fig_ax

    plt.ion()
    x, y = zip(*arr)
    ax.plot(y, x, label = label);
    ax.set(xlabel='time (ns)', ylabel='current (A)')
    #ax.set_ylim(-0.2, np.max(x) + 0.5);
    fig.show();
    ax.grid();

    return fig_ax

def generateAndWriteWaves(numberOfWaves, fileLocation, writeToDPT=False, plot = True):
    '''
    Generates and writes the waveforms to the fileLocation, along with their AGD parameters.
    '''
    fig, ax = plt.subplots();
    df = pd.DataFrame(columns=["A1", "T1", "A2", "T2", "A3", "T3", "amp", "time"])

    if writeToDPT:
        clearDPTFiles()

    for i in range(numberOfWaves):

        wav = genWave()
        time_wav = to_time_domain(wav)
        x, y = zip(*time_wav)
        df.loc[len(df)] ={  "A1": wav[0][1], 
                    "T1": wav[0][0],
                    "A2": wav[1][1],
                    "T2": wav[1][0],
                    "A3": wav[2][1],
                    "T3": wav[2][0],
                    "time": y,
                    "amp": x
        }

        
        input = writeForLTspice(time_wav, name=str(i), plot=False, out_d=fileLocation, writeToDPT=writeToDPT)
        plotA(input, fig_ax=(fig, ax),label=str(i))
    df.to_csv(fileLocation + "/"+ "waveforms.csv", index=False)
    if plot: 
        plt.legend()
        plt.grid()
        plt.show()

    
def applyWaveformsToDPT(path):

    '''
    Applies from path to the waveforms to the DPT directory.
    '''

    clearDPTFiles()
    copy_files(path, DPT_OUT_DIR)
    print("Applied waveforms to DPT directory")

    return 1


def charge_of_pulse():
    print(str(FIRST_PULSE_DURATION) + "ns", str(FIRST_PULSE_AMP) + "A", FIRST_PULSE_DURATION * FIRST_PULSE_AMP, "C")
  
    return FIRST_PULSE_DURATION * FIRST_PULSE_AMP