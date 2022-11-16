import wave
import audioop


# returns bistream if in bitstream mode, None otherwise.
def compress(mode, data, compression):
    if mode == 'b':
            sampWidth = 2
            compressBitstream(data, compression, sampWidth)
    elif mode == 'f':
        compressWav(data, compression)


def compressFromFrames(curFrames, compression, min, max, avg):

    returnFrame = 0b0
    maxAllowable = 32767
    minAllowable = -maxAllowable

    val1 = (curFrames[1] << 8) + curFrames[0]
    val2 = (curFrames[3] << 8) + curFrames[2]

    if (val1 > maxAllowable): val1 -= 2**16
    if (val2 > maxAllowable): val2 -= 2**16

    value = (val1, val2)
    
    maxIncrementer = max/32
    minIncrementer = min/32

    
    j = 0
    for val in value:
        i = 0
        while i < 32:
            if i >= 16:
                if val >= maxIncrementer*i and val <= maxIncrementer*(i+1):
                    addValue = round(val/(compression))
                    if addValue < maxIncrementer*(i-5): addValue = maxIncrementer*(i-5)
                    if addValue > maxIncrementer*(i+6): addValue = maxIncrementer*(i+6)
            else:
                if val >= maxIncrementer*i and val <= maxIncrementer*(i+1):
                    addValue = round(val*(compression))
                    if addValue < maxIncrementer*(i-5): addValue = maxIncrementer*(i-5)
                    if addValue > maxIncrementer*(i+6): addValue = maxIncrementer*(i+6)
            i += 1
        
        i = 0
        while i < 32:
            if i >= 16:
                if val <= minIncrementer*i and val >= minIncrementer*(i+1):
                    addValue = round(val/(compression))
                    if addValue > minIncrementer*(i-5): addValue = minIncrementer*(i-5)
                    if addValue < minIncrementer*(i+6): addValue = minIncrementer*(i+6)
            else:
                if val <= minIncrementer*i and val >= minIncrementer*(i+1):
                    addValue = round(val*(compression))
                    if addValue > minIncrementer*(i-5): addValue = minIncrementer*(i-5)
                    if addValue < minIncrementer*(i+6): addValue = minIncrementer*(i+6)
            i += 1
        if addValue > maxAllowable: addValue = maxAllowable
        if addValue < minAllowable: addValue = minAllowable
        returnFrame = returnFrame + (round(addValue) << 16*j)
        j += 1

    returnFrame = returnFrame.to_bytes(4, "little", signed=True)
    return returnFrame
    



def compressBitstream(bitstream, compression, sampWidth):
    while not (bitstream == None):
        return compressFromFrames(bitstream, compression, sampWidth)
    return None

def compressWav(filename, compression):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nframes = wavRead.getnframes()
    sampWidth = wavRead.getsampwidth()

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())


    frames = wavRead.readframes(nframes)
    (min, max) = audioop.minmax(frames, sampWidth)
    avg = audioop.avg(frames, sampWidth)
    wavRead.rewind()


    readFrame = wavRead.readframes(1)
    i = 0
    while readFrame:
        writeFrame = compressFromFrames(readFrame, compression, min, max, avg)
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
    compress('f', filename, c)




