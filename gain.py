import wave
import audioop

# Written by Harry Poulos z5257055

# returns bistream if in bitstream mode, None otherwise.
def gain(mode, data, gain):
    if mode == 'b':
            sampWidth = 2
            gainBitstream(data, gain, sampWidth)
    elif mode == 'f':
        gainWav(data, gain)


def gainFromFrames(curFrame, gain, sampWidth):
    return(audioop.mul(curFrame, sampWidth, gain))
    
def gainBitstream(bitstream, gain, sampWidth):
    while not (bitstream == None):
        return gainFromFrames(bitstream, gain, sampWidth)
    return None

def gainWav(filename, gain):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nFrames = wavRead.getnframes()

    sampWidth = wavRead.getsampwidth()

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())

    for i in range(nFrames):
        readFrame = wavRead.readframes(1)
        writeFrame = gainFromFrames(readFrame, gain, sampWidth)
        wavWrite.writeframes(writeFrame)
    wavRead.close()
    wavWrite.close()

if __name__ == "__main__":
    print("Enter file name")
    filename = 'Free_Test_Data_500KB_WAV.wav'
    print("Enter gain amount")
    g = input()
    g = float(g)
    gain('f', filename, g)


