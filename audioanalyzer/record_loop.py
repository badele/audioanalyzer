#!/usr/bin/env python

import time
from collections import deque

import pyaudio, wave
import numpy as np

# Audio
BUFFERSIZE = 8192 # Upgragde if you show IOError: [Errno -9981] Input overflowed
NBBYTES = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 120
CUTFRAMES = 100
PYAUDIONBBYTES = {8: 2, 4: 3, 2: 4, 16: 8}


# Misc
MAXSHOWPECTRUM=15000


def audioRecord(prefix='audiorecorded', chunk=8192, formatidx=pyaudio.paInt16, channels=1, rate=44100, silenceduration=1, afterduration=15):

    # Init buffer size
    nbbytesbysecond = rate * PYAUDIONBBYTES[formatidx]

    while True:
        # Init recorder
        bufdatas = deque(maxlen=silenceduration * nbbytesbysecond)
        p = pyaudio.PyAudio()
        stream = p.open(
                format=formatidx, channels=channels, rate=rate, input=True,
                input_device_index=0, frames_per_buffer=chunk
        )

        # Cut first peak sound data during starting record
        stream.read(chunk)


        # Detect threshold noise
        threshold = 500
        recordedframes = []
        level = 0
        while level < threshold:
            # Read audio buffer
            frames = stream.read(chunk)
            bufdatas.extend(frames)

            # Check audio level
            amplitude = np.fromstring(''.join(frames), dtype=np.int16)
            level = np.max(amplitude)
            print "level: %s" % level

        # Before noise detected
        recordedframes.append(''.join(bufdatas))

        # Record audio
        eventtime = time.gmtime()
        nbframes = 0
        nbsilenceframes = 0
        while (nbframes < (afterduration * nbbytesbysecond)) and nbsilenceframes < (silenceduration * nbbytesbysecond):
            # Read audio buffer
            frames = stream.read(chunk)
            bufdatas.extend(frames)
            recordedframes.append(frames)
            nbframes += len(frames)

            # Check audio level
            amplitude = np.fromstring(''.join(bufdatas), dtype=np.int16)
            level = np.max(amplitude)
            print "%s s (%s)" % (int(nbframes/nbbytesbysecond), level)
            if level < threshold:
                nbsilenceframes += len(frames)
            else:
                nbsilenceframes = 0

        # After noise detected
        recordedframes.append(''.join(bufdatas))
        recordedframes = np.fromstring(''.join(recordedframes), dtype=np.int16)

        # Stop recorder
        stream.stop_stream()
        stream.close()
        p.terminate()

        audio = np.array(recordedframes)
        strtime = time.strftime("%Y-%m-%d-%H:%M:%S", eventtime)
        saveWav(np.fromstring(audio, dtype=np.int16), channels=1, rate=RATE, filename='%(prefix)s-%(strtime)s.wav' % locals())


def saveWav(frames, channels, rate, filename):
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(2)
    wavfile.setframerate(rate)
    wavfile.setnframes(len(frames))
    wavfile.writeframes(frames.tostring())
    wavfile.close()

def loadWav(filename):
    wav = wave.open(filename, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
    frames = wav.readframes(nframes * nchannels)

    return {'frames': frames, 'rate': framerate}


# Record Audio
snddata = audioRecord(prefix='audiorecorded', silenceduration=2,chunk=BUFFERSIZE, formatidx=NBBYTES, channels=CHANNELS, rate=RATE)



