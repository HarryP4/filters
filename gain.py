import wave
import struct



def gain(mode, data, gain):
    if mode == 'b':
            maxVol = 2**32
            gainFromBytes(data, gain, maxVol)
    elif mode == 'f':
        gainWav(data, gain)


def gainFromBytes(curByte, gain, maxVol):
    #print(gain)
    if (int.from_bytes(curByte, "little") * gain) <= maxVol*10:
        #print('original = ' + str(int.from_bytes(curByte, "little")))
        #print('new amount should be: ' + str(round(int.from_bytes(curByte, "little") * gain / 100)))
        return(struct.pack('<I', round(int.from_bytes(curByte, "little") * gain / 10)))
    else:
        print("bruh")
        return(struct.pack('<I', round(maxVol/10)))
        
            

def gainWav(filename, gain):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nFrames = wavRead.getnframes()

    maxVol = 2**((wavRead.getsampwidth() * 16))

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())

    for i in range(nFrames):
        writeByte = gainFromBytes(wavRead.readframes(1), gain, maxVol)
        wavWrite.writeframesraw(writeByte)

    wavRead.close()
    wavWrite.close()

    wavRead = wave.open('I' + filename,'rb')
    print(wavRead.readframes(wavRead.getnframes()), file=open('output2.txt', 'w'))
    wavRead.close()

    wavRead = wave.open(filename,'rb')
    print(wavRead.readframes(wavRead.getnframes()), file=open('output.txt', 'w'))
    wavRead.close()

if __name__ == "__main__":
    print("Enter file name")
    filename = 'Free_Test_Data_500KB_WAV.wav'
    print("Enter gain amount")
    g = input()
    g = round(float(g)*10)
    gain('f', filename, g)


