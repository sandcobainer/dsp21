from  scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time

def myTimeConv(x,y): 
    len_x = len(x)
    len_y = len(y)
    y = y[::-1]

    padded_x = np.pad(x, (len_y-1, len_y-1), mode='constant',constant_values=(0,0))
    conv=np.zeros(len_x + len_y - 1, dtype=float)
    
    for lag in range(0, (len_x+len_y-1)):
        conv[lag] = np.sum( np.multiply(padded_x[lag:lag+len_y], y) ) 

    print(conv.dtype)
    return conv

def CompareConv(x, h):
    t1_start = time.time()
    y1 = myTimeConv(x,h)
    t1_end = time.time()

    t2_start = time.time()
    y2 = signal.convolve(x,h,mode='full')
    t2_end = time.time()

    mean_dif = np.mean(y1- y2)
    abs_mean_dif = np.mean(np.abs(y1-y2))
    std_dif = np.std(y1 - y2)
    
    return (mean_dif, abs_mean_dif, std_dif, [t1_end - t1_start, t2_end - t2_start])

def loadSoundFile(filename):
    fs, data = wavfile.read(filename)
    if (data.ndim==2):
        data = data[:,0]
    data = data.astype('float64')
    return fs, data

if __name__ == "__main__":
    fs1, x = loadSoundFile('piano.wav')
    fs2, h = loadSoundFile('impulse-response.wav')
    (md, amd, std, tm) = CompareConv(x, h)

    print(md, amd, std, tm)