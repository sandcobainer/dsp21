from  scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    samples = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    x = amplitude * np.sin(2*np.pi* frequency_Hz * samples + phase_radians)
    t = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=False)
    return t, x

def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    sq = np.zeros(int(sampling_rate_Hz*length_secs))
    for k in range(1,11):
        t,x = generateSinusoidal(amplitude, sampling_rate_Hz, 
                    (2*k-1)*frequency_Hz, length_secs, phase_radians) 
        x = x / (2*k-1)
        sq = sq + x

    sq = sq * (4 / np.pi)
    t = np.linspace(0, length_secs, int(sampling_rate_Hz*length_secs), endpoint=True)
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

    return mag[0:int(len(x)/2)], np.unwrap(ph[0:int(len(x)/2)]), dft.real, dft.imag, np.fft.fftfreq(x.size)[0:int(len(x)/2)]

def generateBlocks(x, sample_rate_Hz, block_size, hop_size): 
    x_b = np.zeros([block_size, int (len(x) / hop_size)+1])
    t = np.array([])
    pad_x = np.append(x, np.zeros(len(x) % block_size)) 
    for block in range(0, len(x), hop_size):
        t = np.append(t, block)
        x_b[:,int(block/hop_size)] = pad_x[block:block+block_size] 
        # print(block)
    
    return t, x_b


def mySpecgram(x,  block_size, hop_size, sampling_rate_Hz, window_type):
    t, x_b = generateBlocks(x, sampling_rate_Hz, block_size, hop_size)
    fr = []
    mag_specgram = np.zeros([ int(block_size/2), x_b.shape[1]])
    print(x_b.shape, mag_specgram.shape)
    if window_type == 'rect':
        r = np.linspace(-10,10,block_size)
        window = np.where(abs(r) < 0.5, 1, 0)
        plt.title('Spectrum with rectangular window')
    elif window_type == 'hann':
        window = np.hanning(block_size)
        plt.title('Spectrum with Hanning window')
    else:
        return 'Invalid window function'

    for b in range(x_b.shape[1]):
        window_x = np.multiply(window , x_b[:, b])
        mag, ph, real, img, fr = computeSpectrum(window_x, sampling_rate_Hz)
        mag_specgram[:,b] = mag
    
    plt.specgram(x ,window = window, NFFT=block_size, Fs = sampling_rate_Hz, 
                noverlap= (block_size-hop_size))
    plt.savefig('results/04-square-rect.png')
    plt.show()
    
    
    return fr, t, mag_specgram

if __name__ == "__main__":
    amp = 1.0
    sr_Hz = 44100 
    frq_Hz = 400
    lnth_secs = 0.5
    ph_rad = 0
    t1, sin = generateSinusoidal(amp, sr_Hz, frq_Hz, lnth_secs, ph_rad)    
    t2, sq = generateSquare(amp, sr_Hz, frq_Hz, lnth_secs, ph_rad)
    block_size = 2048
    hop_size = 1024
    fv, tv, spectrum = mySpecgram(sq, block_size, hop_size, sr_Hz, 'rect')