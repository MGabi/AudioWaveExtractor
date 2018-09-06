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
nrOfWaves = 300


def avgOf(l):
    if len(l) == 0:
        return 0
    return l[0] + avgOf(l[1:])


def mapInterval(audioData, minValue, maxValue):
    for i in range(size(audioData)):
        audioData[i] = np.interp(audioData[i], [minValue, maxValue], [0.0, 1.0])


def saveWaves(file_name, time, audioData):
    global index
    plt.figure(index)
    plt.subplot(211)
    plt.plot(time, audioData, linewidth=1, alpha=0.7, color='#ff7f00')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    file_name = file_name[file_name.index("/") + 1: file_name.index(".wav")]
    outputFile.write(str(index) + " - " + file_name + "\n")
    outputFile.write(str(audioData))
    outputFile.write("\n\n")
    index += 1
    plt.savefig("output/" + file_name + "_ampiltude.png", bbox_inches='tight')


def processSignal(audioFileName):
    rate, audData = wavfile.read(audioFileName)

    channel = audData[:, 0]
    factor = int(round(len(channel) // nrOfWaves))
    timeLine = np.arange(0, float(audData.shape[0] / factor), 1) / rate
    audioData = []
    for i in range(0, size(channel) / factor * factor, factor):
        audioData.append(channel[i])

    maxValue = max(audioData)
    minValue = min(audioData)
    mapInterval(audioData, minValue, maxValue)
    audioData = [round(val, 2) for val in audioData]
    saveWaves(audioFileName, timeLine, audioData)


for fileName in Path("audioFiles//").glob("*.wav"):
    processSignal(str(fileName))

outputFile.close()
