import wave
import numpy
import math
from scipy import signal

# Written by Harry Poulos z5257055
# With code partially copied from https://www.geeksforgeeks.org/digital-low-pass-butterworth-filter-in-python/

# returns bistream if in bitstream mode, None otherwise.
# Call this function to use filters.
def filter(mode, data, filter):
    if mode == 'b':
        return filterBitstream(data, filter)
    elif mode == 'f':
        filterWav(data, filter)
    return None


def filterFromFrames(curFrames, filter):

    returnFrame = 0b0
    maxAllowable = 32767
    minAllowable = -maxAllowable

    values = {'val0': 0, 'val1': 0, 'val2': 0, 'val3': 0, 'val4': 0, 'val5': 0, 'val6': 0, 'val7': 0}

    for i in range(len(values)):
        temp1 = curFrames[i + 1]
        temp2 = curFrames[i]
        values['val' + str(i)] = (int(temp1) << 8) + int(temp2)
        if (values['val' + str(i)] > maxAllowable): values['val' + str(i)] -= 2**16
        if (values['val' + str(i)] > maxAllowable): values['val' + str(i)] -= 2**16



    num, den = signal.butter(2, 0.5)
    
    input = []

    for valKey in values.keys():
        input.append(values[valKey])


    output = signal.lfilter(num, den, input)

    i = 0
    while i < 8:
        returnFrame += (int(output[i + 1]) << 8*(i + 1)) + (int(output[i]) << 8*i)
        i += 2

    returnFrame = round(returnFrame)

    returnFrame = returnFrame.to_bytes(16, "little", signed=True)
    return returnFrame
    


# bistream should be 16 bytes long at a time
# Returns an array of 16 bytes
def filterBitstream(bitstream, filter):
    tempBits = [0]
    tempBits.clear()
    i = 0
    max = 0
    min = 0
    while (i < 16):
        bits = bitstream & (0b11111111 << 8*i)
        if bits > max: max = bits
        if bits < min: min = bits
        i += 1

    while (i < 8):
        bits = bitstream & (0b1111111111111111 << 16*i)
        i += 1
        tempBits.append(filterFromFrames(bits, filter))
    return tempBits

def filterWav(filename, filter):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nframes = wavRead.getnframes()
    sampWidth = wavRead.getsampwidth()

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())


    frames = wavRead.readframes(nframes)
    wavRead.rewind()


    readFrame = wavRead.readframes(4)
    i = 0
    while readFrame:
        writeFrame = filterFromFrames(readFrame, filter)
        wavWrite.writeframes(writeFrame)
        readFrame = wavRead.readframes(4)
        i += 1


    wavRead.close()
    wavWrite.close()

if __name__ == "__main__":
    print("Enter file name")
    filename = 'Free_Test_Data_500KB_WAV.wav'
    print("Enter filter type")
    t = input()
    t = str(t)
    filter('f', filename, t)




