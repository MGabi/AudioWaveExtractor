from math import erf

import scipy

from pathlib import Path
from matplotlib.pylab import *
from scipy.io import wavfile

# Utilitary software to extract a specific number of soundwaves from a .wav
# audio file, together with the height of each wave
#  - nrOfWaves cannot be higher than the size of elements inside the `channel` list
# Usage : place audio .wav file inside the `audioFiles` directory
# Each set of waves can be visualized inside the `output` folder
# Waves heights are placed inside `output/audioWaveHeights.txt` file

outputFile = open("output/audioWaveHeights.txt", "w+")
index = 1
nrOfWaves = 10000

def sigmoid(x):
  return 1 / (1 + math.exp(x))

def avgOf(l):
    sum = 0
    for elem in l:
        sum += elem
    return sum / size(l)


def mapInterval(audioData):
    minReduce = 0.0
    maxReduce = 1.0
    for i in range(size(audioData)):
        # audioData[i] = erf(audioData[i])
        # audioData[i] = arctan(audioData[i])
        audioData[i] = np.interp(audioData[i], [min(audioData), max(audioData)], [0.0, 1.0])
        if audioData[i] >= maxReduce:
            audioData[i] = maxReduce
        if audioData[i] <= minReduce:
            audioData[i] = minReduce
        audioData[i] = np.interp(audioData[i], [minReduce, maxReduce], [0.0, 1.0])

def saveWaves(file_name, time, audioData):
    global index
    plt.figure(index)
    plt.subplot(211)
    # for i in range(size(time)):
    #     plt.plot(time[i], audioData[i], 'bo', markersize=0.5)
    # plt.plot(time, audioData, linewidth=0.8, alpha=0.7, color='#ff7f00')
    for i in range(time.size):
        audioData[i] = 1.0 - audioData[i]
    audioData = [round(val, 3) for val in audioData]
    plt.plot(time, audioData, linewidth=0.8, alpha=0.7, color='#ff7f00')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    file_name = file_name[file_name.index("/") + 1: file_name.index(".wav")]
    print fileName
    print audioData
    outputFile.write(str(index) + " - " + file_name + "\n")
    outputFile.write(str(audioData))
    outputFile.write("\n\n")
    index += 1
    plt.savefig("output/" + file_name + "_ampiltude.png",
                bbox_inches='tight',
                dpi=300)


def processSignal(audioFileName):
    rate, audData = wavfile.read(audioFileName)

    channel = audData[:, 0]
    factor = int(round(len(channel) // nrOfWaves))
    timeLine = np.arange(0, float(audData.shape[0] / factor), 1) / rate
    audioData = []
    for i in range(0, size(channel) / factor * factor, factor):
        # audioData.append(avgOf(channel[i:i+factor]))
        audioData.append(channel[i])

    mapInterval(audioData)
    audioData = [round(val, 3) for val in audioData]
    saveWaves(audioFileName, timeLine, audioData)


for fileName in Path("audioFiles//").glob("*.wav"):
    processSignal(str(fileName))
    break

outputFile.close()
