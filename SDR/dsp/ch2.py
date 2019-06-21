import ThinkDSP.code.thinkdsp as tdsp
import ThinkDSP.code.thinkplot as tplot

import matplotlib.pyplot as plt
import numpy as np


def main():
    SawtoothChirpTest()

def specgram():
    chp = tdsp.Chirp(start=220, end=880)
    wave = chp.make_wave(duration=1)
    # wave.write('chirp.wav')
    # wave.make_spectrum().plot()

    echp = tdsp.ExpoChirp(start=220, end=880)
    wave = echp.make_wave(duration=1)
    # wave.write('expo_chirp.wav')
    wave.make_spectrum().plot()

    # specgram = wave.make_spectrogram(seg_length=512)
    # specgram.plot(high=1500)

    plt.show()

def spec_leakage():
    sig = tdsp.CosSignal(freq=440)
    wave = sig.make_wave(duration=30.5*sig.period)
    # wave.plot()
    wave.make_spectrum().plot()

    # windows: Bartlett(M), Blackman(M), Hamming(M), Hanning(M), Kaiser(M, beta)
    # window = np.bartlett(len(wave))
    # window = np.blackman(len(wave))
    # window = np.hamming(len(wave))
    # window = np.hanning(len(wave))
    window = np.kaiser(len(wave), 8.6)
    wave.window(window)
    wave.make_spectrum().plot()

    plt.show()

def vowels():
    

def SawtoothChirpTest():
    sig = SawtoothChirp(440, 880, 1)
    wave = sig.make_wave(duration=1, start=0, framerate=20000)
    # seg = wave.segment(start=0, duration=(30/440))
    # wave.plot()

    # wave.make_spectrum().plot()
    wave.make_spectrogram(seg_length=512).plot()

    plt.show()

class SawtoothChirp(tdsp.Chirp):
    def evaluate(self, ts):
        freqs = np.linspace(self.start, self.end, len(ts))
        cycles = freqs * ts
        frac, _ = np.modf(cycles)
        ys = tdsp.normalize(tdsp.unbias(frac), self.amp)
        return ys

if __name__ == "__main__":
    main()