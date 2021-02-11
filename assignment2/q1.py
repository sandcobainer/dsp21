from  scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def myTimeConv(x,y): 
    len_x = len(x)
    len_y = len(y)
    y = y[::-1]

    padded_x = np.pad(x, (len_y-1, len_y-1), mode='constant',constant_values=(0,0))
    conv=np.zeros(len_x + len_y - 1)
    
    for lag in range(0, (len_x+len_y-1)):
        co = np.sum( np.multiply(padded_x[lag:lag+len_y], y) )
        conv[lag] = co   

    return conv

if __name__ == "__main__":
    x = np.ones(200)
    h1 = np.linspace(0,1,26)
    h2 = np.linspace(1,0,26)
    h = np.append(h1, h2[1:])
    
    y =  myTimeConv(x,h) 

    plt.plot(y)
    plt.xlabel('Padded signal of length')
    plt.ylabel('Convolution: x * h')
    plt.savefig('results/01-convolution.png')
    plt.show()
    