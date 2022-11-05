import wave
import audioop


# returns bistream if in bitstream mode, None otherwise.
def compress(mode, data, compression):
    if mode == 'b':
            sampWidth = 2
            compressBitstream(data, compression, sampWidth)
    elif mode == 'f':
        compressWav(data, compression)


def compressFromFrames(curFrames, compression, sampWidth):
    (min, max) = audioop.minmax(curFrames, sampWidth)

    avg = audioop.avg(curFrames, sampWidth)
    curval = int.from_bytes(curFrames, "little")
    
    mask1 = 0b000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111
    mask2 = 0b000000000000000000000000000000000000000000000000000000000000000000000000111111111111000000000000
    mask3 = 0b000000000000000000000000000000000000000000000000000000000000111111111111000000000000000000000000
    mask4 = 0b000000000000000000000000000000000000000000000000111111111111000000000000000000000000000000000000
    mask5 = 0b000000000000000000000000000000000000111111111111000000000000000000000000000000000000000000000000
    mask6 = 0b000000000000000000000000111111111111000000000000000000000000000000000000000000000000000000000000
    mask7 = 0b000000000000111111111111000000000000000000000000000000000000000000000000000000000000000000000000
    mask8 = 0b111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000


    val1 = (curval & mask1)
    val2 = ((curval & mask2) >> 12)
    val3 = ((curval & mask3) >> 24)
    val4 = ((curval & mask4) >> 36)
    val5 = ((curval & mask5) >> 48)
    val6 = ((curval & mask6) >> 60)
    val7 = ((curval & mask7) >> 72) 
    val8 = ((curval & mask8) >> 84)


    value = (val1, val2, val3, val4, val5, val6, val7, val8)
    returnFrame = 0b0
    i = 0
    maxAllowable = 4095
    for val in value:
        addValue = None
        if val <= avg/2 and val >= min:
            addValue = round(val*(1.2*compression))
            if addValue > maxAllowable: addValue = maxAllowable
        elif val >= avg/2 and val <= avg:
            addValue = round(val*(1.1*compression))
            if addValue > maxAllowable: addValue = maxAllowable
        elif val >= avg and val <= 1.5*avg:
            addValue = round(val*(1/compression))
            if addValue > maxAllowable: addValue = maxAllowable
        elif val >= 1.5*avg and val <= max:
            addValue = round(val*(1/(1.1*compression)))
            if addValue > maxAllowable: addValue = maxAllowable
        elif addValue is None: 
            addValue = round(val)
        returnFrame = returnFrame | addValue << 12*i
        i += 1
    returnFrame = returnFrame.to_bytes(12, "little")
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

    readFrame = wavRead.readframes(4)
    i = 0
    while readFrame:
        writeFrame = compressFromFrames(readFrame, compression, sampWidth)
        wavWrite.writeframes(writeFrame)
        readFrame = wavRead.readframes(4)
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


