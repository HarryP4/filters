import wave
import audioop



# returns bistream if in bitstream mode, None otherwise.
def filter(mode, data, gain):
    if mode == 'b':
            sampWidth = 2
            filterBitstream(data, gain, sampWidth)
    elif mode == 'f':
        filterWav(data, gain)


def filterFromFrames(curFrame, gain, sampWidth):
    return(audioop.mul(curFrame, sampWidth, gain))
    

def filterBitstream(bitstream, gain, sampWidth):
    while not (bitstream == None):
        return filterFromFrames(bitstream, gain, sampWidth)
    return None


def filterWav(filename, gain):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nFrames = wavRead.getnframes()

    sampWidth = wavRead.getsampwidth()

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())

    for i in range(nFrames):
        readFrame = wavRead.readframes(1)
        writeFrame = filterFromFrames(readFrame, gain, sampWidth)
        wavWrite.writeframes(writeFrame)

    wavRead.close()
    wavWrite.close()

