import pyaudio, wave

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import scipy.fftpack as fftpack

import numpy as np


def note(freq, len=1, rate=44100, amp=1):
    t = np.linspace(0, len, len * rate)
    data = np.sin(2 * np.pi * freq * t) * amp
    return data.astype(np.int16)


def audioRecord(chunk=8192, format=pyaudio.paInt16, channels=1, rate=44100, record_seconds=1):
    # Init recorder
    p = pyaudio.PyAudio()
    stream = p.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
            input_device_index=0, frames_per_buffer=BUFFERSIZE
    )

    # Get sound datas
    frames = []
    for i in range(0, int(RATE / BUFFERSIZE * RECORD_SECONDS)):
        if i % (RATE / BUFFERSIZE) == 0:
            print (i / (RATE / BUFFERSIZE)) + 1
        data = stream.read(BUFFERSIZE)
        frames.append(data)
    frames = ''.join(frames)

    # Stop recorder
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames


def saveWav(snddata, filename):
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(snddata)
    wavfile.close()

def loadWav(filename):
    wav = wave.open(filename, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes(nframes * nchannels)

    return frames

########################################
# Main
########################################


BUFFERSIZE = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2
CUTFRAMES = 100

# Record Audio
snddata = audioRecord(
        chunk=BUFFERSIZE, format=FORMAT,channels=CHANNELS,
        rate=RATE, record_seconds=RECORD_SECONDS
)

# Create tone
# snddata = note(freq=440, len=RECORD_SECONDS*2, amp=32728, rate=RATE)

# Load sound
#snddata = loadWav('440.wav')


# Amplitude
amplitude = np.fromstring(snddata[CUTFRAMES:], np.int16)/32768.0
absamplitude = np.abs(amplitude)

# Spectrum
fftn = 8192
ffty = np.abs(np.fft.fft(amplitude,n=fftn))
fftx = np.fft.fftfreq(len(ffty), 1/float(RATE))

# Specgram
S, freqs, bins, im = plt.specgram(amplitude, NFFT=1024, noverlap=512, Fs=RATE)

gs = gridspec.GridSpec(12, 12)

# Amplitude
ax1 = plt.subplot(gs[0:4,6:])
ax1.set_title('Timeline')
ax1.set_ylabel('Amplitude')
ax1.set_xlabel('Time (s)')
ax1.grid(True)
ax1.plot(amplitude, color='black')

# Spectrum
ax2 = plt.subplot(gs[6:,6:])
ax2.set_title('Spectrum')
ax2.set_ylabel('A')
ax2.set_xlabel('F (Hz)')
ax2.grid(True)
ax2.plot(fftx, ffty,c='k')
ax2.axis([0,RATE/2.0,0,ffty.max()])

# Specgram
ax3 = plt.subplot(gs[:,0:5])
ax3.set_title('Specgram')
ax3.set_ylabel('F (Hz)')
ax3.set_xlabel('Time (s)')
ax3.grid(True)
ax3.specgram(amplitude, NFFT=fftn, noverlap=512, Fs=RATE,cmap=plt.cm.gray_r)


plt.savefig('graph.png', dpi=300)
plt.show()




