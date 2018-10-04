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
nrOfWaves = 5000


def sigmoid(x):
    return 1 / (1 + math.exp(x))


def avg_of(l):
    sum = 0
    for elem in l:
        sum += elem
    return sum / size(l)


def map_interval(audioData):
    min_reduce = 0.35
    max_reduce = 1.0
    # for i in range(size(audioData)):
    #     audioData[i] = np.interp(audioData[i], [min(audioData), max(audioData)], [0.0, 1.0])
        # if audioData[i] >= max_reduce:
        #     audioData[i] = max_reduce
        # if audioData[i] <= min_reduce:
        #     audioData[i] = min_reduce

    for i in range(size(audioData) - 1):
        audioData[i] = abs(audioData[i] - audioData[i+1])

    # for i in range(size(audioData)):
    #     audioData[i] = np.interp(audioData[i], [min(audioData), max(audioData)], [0.0, 1.0])
    #
    for i in range(size(audioData)):
        audioData[i] = round(np.interp(audioData[i], [min(audioData), max(audioData)], [min_reduce, max_reduce]), 5)


def save_waves(file_name, time, audioData):
    global index
    plt.figure(index)
    plt.subplot(211)
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


def process_signal(audioFileName):
    rate, audData = wavfile.read(audioFileName)

    channel = audData[:, 0]
    factor = int(round(len(channel) // nrOfWaves))
    timeLine = np.arange(0, float(audData.shape[0] / factor), 1) / rate
    audioData = []
    for i in range(0, size(channel) / factor * factor, factor):
        # audioData.append(avgOf(channel[i:i+factor]))
        audioData.append(channel[i])

    map_interval(audioData)
    save_waves(audioFileName, timeLine, audioData)


for fileName in Path("audioFiles//").glob("*.wav"):
    process_signal(str(fileName))

outputFile.close()
