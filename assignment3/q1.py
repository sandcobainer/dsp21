from  scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    samples = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    x = amplitude * np.sin(2*np.pi*frequency_Hz * samples + phase_radians)
    t = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    return t, x


if __name__ == "__main__":
    amp = 1.0
    sr_Hz = 44100 
    frq_Hz = 400
    lnth_secs = 0.5
    ph_rad = np.pi/2

    t,x = generateSinusoidal(amp, sr_Hz, frq_Hz, lnth_secs, ph_rad)
    
    plt.plot(t[:int(sr_Hz*0.005)], x[:int(sr_Hz*0.005)])
    plt.xlabel('Sine Signal in seconds')
    plt.ylabel('Amplitude')
    plt.savefig('results/01-sinewave.png')
    plt.show()
    