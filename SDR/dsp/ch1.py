import ThinkDSP.code.thinkdsp as tdsp
import ThinkDSP.code.thinkplot as tplot

import matplotlib.pyplot as plt
import numpy as np


def main():
    evenOddSqr()

def start():
    cos_sig = tdsp.CosSignal(freq=440, amp=1.0, offset=0)
    cos2 = tdsp.CosSignal(freq=333, amp=1.0, offset=0)
    sin_sig = tdsp.SinSignal(freq=880, amp=0.5, offset=0)
    mix = cos_sig + sin_sig + cos2
    wave = mix.make_wave(duration=10, start=0, framerate=11025)
    spectrum = wave.make_spectrum()
    spectrum.plot()
    # wave.write('1.wav')
    # wave.plot()

    period = mix.period
    seg = wave.segment(start=0, duration=3*period)
    # seg.plot()

    plt.show()

def triSqr():
    tri = tdsp.TriangleSignal(200)
    # tri.plot()

    # tri_wave = tri.make_wave(duration=0.5, framerate=10000)
    # tri_wave.ys += 1
    # tri_seg = tri_wave.segment(start=0, duration=3*tri.period)
    # tri_seg.plot()
    # tri_spec = tri_wave.make_spectrum()
    # tri_spec.plot()

    sqr = tdsp.SquareSignal(200)
    # sqr.plot()

    sqr_spec = sqr.make_wave(duration=0.5, framerate=10000).make_spectrum()
    sqr_spec.plot()

    plt.show()

def aliasing():
    # tri = tdsp.TriangleSignal(1100)
    # tri_spec = tri.make_wave(duration=0.5, framerate=10000).make_spectrum()
    # tri_spec.plot()

    # sig_o = tdsp.CosSignal(4500)
    # period = sig_o.period*5
    # sig_o_wave = sig_o.make_wave(duration=period, framerate=10000)
    # sig_o_spec = sig_o_wave.make_spectrum()
    # # sig_o_spec.plot()
    # sig_o_wave.plot()
    # # sig_o.make_wave(duration=period, framerate=100000).plot()

    # sig_t = tdsp.CosSignal(5500)
    # sig_t_wave = sig_t.make_wave(duration=period, framerate=10000)
    # sig_t_spec = sig_t_wave.make_spectrum()
    # # sig_t_spec.plot()
    # sig_t_wave.plot()
    # sig_t.make_wave(duration=period, framerate=100000).plot()

    sqr = tdsp.SquareSignal(freq=1100)
    sqr_seg = sqr.make_wave(duration=5, framerate=7000)
    sqr_spec = sqr_seg.make_spectrum()
    # sqr_spec.plot()
    sqr_wave = sqr_spec.make_wave()
    sqr_wave.segment(start=0, duration=sqr.period*3).plot()
    sqr.make_wave(duration=sqr.period*3, framerate=60000).plot()
    # sqr_seg.write('aliased_sqr.wav')

    plt.show()

def sounds():
    wave = tdsp.read_wave('ThinkDSP/code/92002__jcveliz__violin-origional.wav')
    # wave.plot()
    spect = wave.make_spectrum()
    # spect.plot()
    spect.low_pass(cutoff=3000, factor=0.01)
    spect.plot()
    wave_low = spect.make_wave()
    wave_low.write('violin_low2.wav')
    plt.show()

def mod():
    carrier = tdsp.CosSignal(freq=440, amp=1.0, offset=0)
    usb = tdsp.CosSignal(freq=480, amp=0.5, offset=0)
    lsb = tdsp.CosSignal(freq=400, amp=0.5, offset=0)
    mix = carrier + usb + lsb
    wave = mix.make_wave(duration=0.2, start=0, framerate=11025)
    # wave.write('mod.wav')
    # wave.plot()

    seg = wave.segment(start=0, duration=20*mix.period)
    # seg.plot()

    msg = tdsp.CosSignal(freq=40, amp=1.0, offset=0)
    seg_msg = msg.make_wave(duration=20*mix.period)
    # seg_msg.ys += 1
    # seg_msg.plot()

    spectr = wave.make_spectrum()
    # spectr.plot()
    # spectr.high_pass(cutoff=460, factor=0.01)
    spectr.band_stop(low_cutoff=420, high_cutoff=460, factor=0.5)
    spectr.high_pass(cutoff=420, factor=0.2)
    # spectr.plot()

    wave_low = spectr.make_wave()
    # wave_low.plot()

    seg_high = wave_low.segment(start=0, duration=20*mix.period)
    seg_high.plot()

    seg_msg.ys = seg_msg.ys*0.5+0.5
    seg_msg.plot()

    plt.show()

def fsDivHsTest():
    tri = tdsp.SawtoothSignal(freq=440)
    seg = tri.make_wave(duration=1)
    seg.write('fsDivHs0.wav')
    # seg.plot()

    spec = seg.make_spectrum()
    spec.plot()
    fsDivHs(spec)
    # spec.plot()

    wave = spec.make_wave()
    wave.write('fsDivHs.wav')
    # wave.plot()

    plt.show()

def fsDivHs(spec):
    # spec.hs[0] = 0
    # print(spec.hs[spec.fs < 200])
    spec.fs[0] = 1
    spec.hs = np.true_divide(spec.hs, spec.fs)
    spec.fs[0] = 0
    spec.hs *= 500
    spec.plot()
    # spec.

def evenOddSqr():
    saw = tdsp.SquareSignal(freq= 100)
    spec = saw.make_wave(duration=1).make_spectrum()
    # print(spec.hs[spec.fs < 0])
    # spec.plot()
    # spec.hs = np.true_divide(spec.hs, np.arange(len(spec.fs)), where=spec.fs % 100 == 0)
    # spec.plot()

    n = 6000
    a = np.arange(0, n, 10)
    b = np.arange(0, n, 10)

    mask = (a%100 == 0)

    b = 10000/(b**2)
    b[0] = 0
    b[~mask] = 0

    spec.hs = b*1000
    spec.fs = a

    # spec.plot()
    tplot.plot(spec.fs, spec.angles)

    wave = spec.make_wave()
    # wave.segment(start=0, duration=saw.period*5).plot()
    # wave.make_spectrum().plot()

    wave.ys = -wave.ys
    # wave.segment(start=0, duration=saw.period*5).plot()

    spec = wave.make_spectrum()
    # tplot.plot(spec.fs, spec.angles)
    
    # spec.make_wave().segment(duration=saw.period*5).plot()
    # spec.plot()
    # tplot.plot(spec.fs, spec.angles)

    # print(a)
    # print(b)

    plt.show()

def sawTest():
    saw = SawTooth(freq=100)
    seg = saw.make_wave(duration=0.5, framerate=10000)
    # seg.plot()
    spec = seg.make_spectrum()
    spec.plot()

    plt.show()

class SawTooth(tdsp.Sinusoid):
    def evaluate(self, ts):
        ts = np.asarray(ts)
        cycles = self.freq * ts + self.offset / tdsp.PI2
        frac, _ = np.modf(cycles)
        ys = tdsp.normalize(tdsp.unbias(frac), self.amp)
        return ys

if __name__ == "__main__":
    main()