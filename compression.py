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

    curval = int.from_bytes(curFrames, "little")
    
    mask1 = 0b111111111111
    mask2 = mask1 << 12
    mask3 = mask2 << 12
    mask4 = mask3 << 12
    mask5 = mask4 << 12
    mask6 = mask5 << 12
    mask7 = mask6 << 12
    mask8 = mask7 << 12


    val1 = (curval & mask1)
    val2 = ((curval & mask2) >> 12)
    #val3 = ((curval & mask3) >> 12)
    #val4 = ((curval & mask4) >> 8)

 
    (localmin, localmax) = audioop.minmax(curFrames, 2)



    value = (val1, val2)
    returnFrame = 0b0
    i = 0
    maxAllowable = 32767
    minAllowable = -maxAllowable
    for val in value:
        addValue = None
        if val <= avg/2 and val >= min:
            addValue = round(val*1.1*compression)
            if addValue > maxAllowable: addValue = maxAllowable
            if addValue < minAllowable: addValue = minAllowable
        elif val >= avg/2 and val <= avg:
            addValue = round(val*compression)
            if addValue > maxAllowable: addValue = maxAllowable
            if addValue < minAllowable: addValue = minAllowable
        elif val >= avg and val <= 1.5*avg:
            addValue = round(val/compression)
            if addValue > maxAllowable: addValue = maxAllowable
            if addValue < minAllowable: addValue = minAllowable
        elif val >= 1.5*avg and val <= max:
            addValue = round(val/(1.1*compression))
            if addValue > maxAllowable: addValue = maxAllowable
            if addValue < minAllowable: addValue = minAllowable
        elif addValue is None: 
            addValue = round(val)
        returnFrame = returnFrame | (addValue << 12*i)
        i += 1
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


