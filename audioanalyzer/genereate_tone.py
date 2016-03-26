#!/usr/bin/env python

import pyaudio, wave
import numpy as np


def tone(freq, seconds=1, rate=44100, amp=1):
    t = np.linspace(0, seconds, seconds * rate)
    data = np.sin(2 * np.pi * freq * t) * amp
    return np.array(data, np.int16)


def saveWav(frames, channels, rate, filename):
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(2)
    wavfile.setframerate(rate)
    wavfile.setnframes(len(frames))
    wavfile.writeframes(frames.tostring())
    wavfile.close()


########################################
# Main
########################################

# tones parameters
tones = []
rate = 44100
maxamp = 32728
nbstep = 8
freqlow=440
freqhight=4000


# Create tones
tones.append(tone(freq=440, seconds=1, amp=0, rate=rate))
nbloop = 0
for amp in np.linspace(maxamp/nbstep, maxamp, nbstep):

    nbloop += 1
    for repeat in range(0,nbloop):
        tones.append(tone(freq=freqlow, seconds=0.2, amp=amp, rate=rate))
        tones.append(tone(freq=freqlow, seconds=0.8, amp=0, rate=rate))

    tones.append(tone(freq=440, seconds=1, amp=0, rate=rate))

    for repeat in range(0,nbloop):
        tones.append(tone(freq=freqhight, seconds=0.2, amp=amp, rate=rate))
        tones.append(tone(freq=freqhight, seconds=0.8, amp=0, rate=rate))

    tones.append(tone(freq=440, seconds=3, amp=0, rate=rate))


# Save tones
snddata = np.concatenate(tones)
saveWav(np.fromstring(snddata, dtype=np.int16), channels=1, rate=rate, filename='tones.wav')