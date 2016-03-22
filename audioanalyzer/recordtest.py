import pyaudio, wave
import matplotlib.pyplot as plt
import numpy as np


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
        print i
        data = stream.read(BUFFERSIZE)
        frames.append(data)
    frames = ''.join(frames)

    # Stop recorder
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames


def toWav(snddata, filename):
    wavfile = wave.open(filename, 'wb')
    wavfile.setnchannels(CHANNELS)
    wavfile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wavfile.setframerate(RATE)
    wavfile.writeframes(snddata)
    wavfile.close()


def toGraph(snddata, filename):
    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(snddata, np.int16)

    s.plot(amplitude)
    fig.savefig(filename)


########################################
# Main
########################################


BUFFERSIZE = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3

snddata = audioRecord(
        chunk=BUFFERSIZE, format=FORMAT,channels=CHANNELS,
        rate=RATE, record_seconds=RECORD_SECONDS
)
toWav(snddata, "Audio.wav")
toGraph(snddata, "graph.png")



