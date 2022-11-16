import wave
import audioop

# Written by Harry Poulos z5257055

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

    val1 = (curFrames[1] << 8) + curFrames[0]
    val2 = (curFrames[3] << 8) + curFrames[2]

    if (val1 > maxAllowable): val1 -= 2**16
    if (val2 > maxAllowable): val2 -= 2**16

    value = (val1, val2)
    

    returnFrame = returnFrame.to_bytes(4, "little", signed=True)
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


    readFrame = wavRead.readframes(1)
    i = 0
    while readFrame:
        writeFrame = filterFromFrames(readFrame, filter)
        wavWrite.writeframes(writeFrame)
        readFrame = wavRead.readframes(1)
        i += 1


    wavRead.close()
    wavWrite.close()

if __name__ == "__main__":
    print("Enter file name")
    filename = 'Free_Test_Data_500KB_WAV.wav'
    print("Enter compress amount")
    c = input()
    c = float(c)
    filter('f', filename, c)




