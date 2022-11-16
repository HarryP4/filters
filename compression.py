import wave
import audioop

# Written by Harry Poulos z5257055

# returns bistream if in bitstream mode, None otherwise.
# Call this function to use Compression.
def compress(mode, data, compression):
    if compression == 0: compression = 0.0001
    if mode == 'b':
            return compressBitstream(data, compression)
    elif mode == 'f':
        compressWav(data, compression)
    return None


def compressFromFrames(curFrames, compression, min, max):

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
    


# bistream should be 16 bytes long at a time
# Returns an array of 16 bytes
def compressBitstream(bitstream, compression):
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
        tempBits.append(compressFromFrames(bits, compression, min, max))
    return tempBits

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
    wavRead.rewind()


    readFrame = wavRead.readframes(1)
    i = 0
    while readFrame:
        writeFrame = compressFromFrames(readFrame, compression, min, max)
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




