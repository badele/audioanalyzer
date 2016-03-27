#!/usr/bin/env python

import pyaudio, wave

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np

# parameters
MAXSHOWPECTRUM=15000


def loadWav(filename):
    wav = wave.open(filename, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes(nframes * nchannels)

    return {'frames': frames, 'rate': framerate}


# Load sound
sndinfo = loadWav('audio.wav')
snddata = sndinfo['frames']
rate = sndinfo['rate']


# Amplitude
snddata = snddata[:(len(snddata)/int(rate))*rate]
amplitude = np.fromstring(snddata, np.int16)/32768.0
totaltime = len(amplitude)/float(rate)
t = np.linspace(0, totaltime, len(amplitude))


# plot parameters
gs = gridspec.GridSpec(12, 13)
axamplitude = plt.subplot(gs[0:3, :-4])
axspecgram = plt.subplot(gs[4:, :-4], sharex=axamplitude)
axspectrum = plt.subplot(gs[4:, 9:12],sharey=axspecgram)
axcolorbar = plt.subplot(gs[4:, 12])
cmap = plt.get_cmap('viridis')
cmap.set_under(color='k', alpha=None)

# Amplitude
axamplitude.set_title('Timeline')
axamplitude.set_ylabel('Amplitude')
axamplitude.set_xlabel('Time (s)')
axamplitude.grid(True)

axamplitude.plot(t, amplitude, color='#482576')
axamplitude.axis([0, totaltime, -np.max(np.abs(amplitude)), np.max(np.abs(amplitude))])

# # Spectrum
fftn = 4096
fftamplitude = 20*np.log10(np.abs(np.fft.fft(amplitude,n=fftn))/np.max(amplitude))
fftfreqs = np.fft.fftfreq(len(fftamplitude), 1/float(rate))

axspectrum.set_title('Spectrum')
axspectrum.set_ylabel('')
axspectrum.set_xlabel('dB')
axspectrum.grid(True)

axspectrum.fill_between(fftamplitude,0,fftfreqs, color='#482576')
axspectrum.axis([0,np.max(fftamplitude),0,MAXSHOWPECTRUM])


# Specgram
axspecgram.set_title('Specgram')
axspecgram.set_ylabel('F (Hz)')
axspecgram.set_xlabel('Time (s)')
axspecgram.grid(True)

Pxx, freqs, bins, im = axspecgram.specgram(amplitude, Fs=rate, NFFT=64, noverlap=32, cmap=cmap, vmin=-150, scale_by_freq=True)
plt.colorbar(im, cax=axcolorbar, label='Intensity in dB')
axspecgram.axis([0, totaltime, 0, MAXSHOWPECTRUM])

plt.savefig('graph.png', dpi=300)
plt.show()




