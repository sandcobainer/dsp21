from  scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    samples = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    x = amplitude * np.sin(2*np.pi* frequency_Hz * samples + phase_radians)
    t = np.linspace(0, length_secs, len(samples), endpoint=False)
    return t, x

def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    sq = np.zeros(int(sampling_rate_Hz*length_secs))
    for k in range(1,11):
        t,x = generateSinusoidal(amplitude, sampling_rate_Hz, 
                    (2*k-1)*frequency_Hz, length_secs, phase_radians) 
        x = x / (2*k-1)
        sq = sq + x

    sq = sq * (4 / np.pi)
    t = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    return t, sq

def computeSpectrum(x, sample_rate_Hz):
    # 3.4 frequency resolution = sample rate / duration of signal in samples
    # ie. 44100 / len(x)

    # 3.5 If we zero-pad the signal the same number of zeros as the length of the signal, 
    # frequency resolution = sample rate / 2 * len(x)
    # Thus the frequency bins become narrower in size resulting in increased frequency resolution
    # on the DFT 
    dft = np.fft.fft(x) 
    mag = np.abs(dft) / len(x)
    ph = np.angle(dft)
    fr = np.linspace(0, sample_rate_Hz/2, int(len(x)/2))

    return mag[0:int(len(x)/2)], ph[0:int(len(x)/2)], dft.real, dft.imag, fr   


if __name__ == "__main__":
    amp = 1.0
    sr_Hz = 44100 
    frq_Hz = 400
    lnth_secs = 0.5
    ph_rad = 0

    t1, sin = generateSinusoidal(amp, sr_Hz, frq_Hz, lnth_secs, ph_rad)
    t2, sq = generateSquare(amp, sr_Hz, frq_Hz, lnth_secs, ph_rad)
    
    mag, ph, real, img, fr = computeSpectrum(sq, sr_Hz)
    print(mag.shape, fr.shape)
    fig, [ax1,ax2] = plt.subplots(1, 2)
    ax1.set_title('Magnitude Spectrum')
    ax2.set_title('Phase Spectrum')
    ax1.plot(fr, mag)
    ax2.plot(fr, ph)
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Amplitude')
    
    ax2.set_xlabel('Frequency (Rad)')
    ax2.set_ylabel('Amplitude')
    
    plt.savefig('results/03-squarewave.png')
    plt.show()
    