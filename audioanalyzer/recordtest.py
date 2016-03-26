#!/usr/bin/env python

import pyaudio, wave

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np


def audioRecord(chunk=8192, format=pyaudio.paInt16, channels=1, rate=44100, record_seconds=1,cutframes=100):
    # Init recorder
    p = pyaudio.PyAudio()
    stream = p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
            input_device_index=0, frames_per_buffer=BUFFERSIZE
    )

    # Get sound datas
    frames = []
    for i in range(0, int(rate / BUFFERSIZE * RECORD_SECONDS)):
        if i % (rate / BUFFERSIZE) == 0:
            print "%s seconds" % int((i / (rate / BUFFERSIZE)) + 1)
        data = stream.read(BUFFERSIZE)
        frames.append(data)
    frames = ''.join(frames)

    # Stop recorder
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames[CUTFRAMES:]


def saveWav(frames, channels, rate, filename):
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(2)
    wavfile.setframerate(rate)
    wavfile.setnframes(len(frames))
    wavfile.writeframes(frames)
    wavfile.close()

def loadWav(filename):
    wav = wave.open(filename, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes(nframes * nchannels)

    return {'frames': frames, 'rate': framerate}



########################################
# Main
########################################


# Audio
BUFFERSIZE = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
CUTFRAMES = 100

# Misc
MAXSHOWPECTRUM=15000

# Record Audio
snddata = audioRecord(
        chunk=BUFFERSIZE, format=FORMAT,channels=CHANNELS,
        rate=RATE, record_seconds=RECORD_SECONDS,cutframes=CUTFRAMES
)
saveWav(snddata, CHANNELS, RATE, 'audio.wav')
rate = RATE

# Load sound
# sndinfo = loadWav('440.wav')
# snddata = sndinfo['frames']
# rate = sndinfo['rate']


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




