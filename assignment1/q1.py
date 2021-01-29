from  scipy.io import wavfile
from scipy.signal import correlate
import numpy as np
import matplotlib.pyplot as plt

def crossCorr(x,y):
    len_x = len(x)
    len_y = len(y)
    padded_x = np.pad(x, (len_y-1, len_y-1), mode='constant',constant_values=(0,0))
    corr=np.zeros(len(padded_x))
    for lag in range(0, (len_x+len_y-1)):
        co = np.sum( np.multiply(padded_x[lag:lag+len_y], y) )
        corr[lag] = co   
    return corr


def loadSoundFile(filename):
    fs, data = wavfile.read(filename)
    if (data.shape[1]==2):
        data = data[:,0]
    data = data.astype('float32')
    return fs, data

if __name__ == "__main__":
    fs1, snare = loadSoundFile('snare.wav')
    fs2, loop = loadSoundFile('drum_loop.wav')
    
    corr = crossCorr(loop,snare)
    corr = corr / np.max(corr)
    plt.plot(corr)
    plt.xlabel('Lag (Loop signal padded on both ends)')
    plt.ylabel('Normalized correlation')


    plt.savefig('results/01-correlation.png')
    plt.show()
    