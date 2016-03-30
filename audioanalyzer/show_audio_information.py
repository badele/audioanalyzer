#!/usr/bin/env python

import pyaudio, wave

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec

import numpy as np


def loadWav(filename):
    wav = wave.open(filename, "r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    frames = np.fromstring(wav.readframes(nframes * nchannels), np.int16)

    return {'frames': frames, 'rate': framerate, 'samplewidth': sampwidth}


def rms(signal):
    return np.sqrt(np.mean(np.square(signal)))


def percent(signal, maxvalue=None):
    if not maxvalue:
        maxvalue = np.max(np.abs(signal))

    return (signal / float(maxvalue)) * 100


def audio_information(sndinfo):
    frames = sndinfo['frames']
    rate = sndinfo['rate']
    samplewidth = sndinfo['samplewidth']
    nbframes = len(frames)
    maxwavamplitude = (2 ** (samplewidth * 8)) / 2

    amplitude = percent(frames, maxwavamplitude)
    totaltime = len(amplitude) / float(rate)
    rmssignal = rms(amplitude)
    maxsignal = np.max(np.abs(amplitude))
    meansignal = np.mean(np.abs(amplitude))
    stdsignal = np.std(np.abs(amplitude))

    print "Audio file information"
    print "----------------------"
    print "Duration: %.2f s" % totaltime
    print "Frames: %s frames" % nbframes
    print "Rate: %s Hz" % rate
    print "Max amplitude value: %s" % maxwavamplitude
    print ""

    print "Sound information"
    print "-----------------"
    print "Max amplitude in percent %.4f" % maxsignal
    print "RMS: %.4f" % rmssignal
    print "Mean: %.4f" % meansignal
    print "STD: %.4f" % stdsignal


# Load sound
FILENAME = 'silence'
frames = loadWav('%(FILENAME)s.wav' % locals())
audio_information(frames)



