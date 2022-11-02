import wave
import struct



def compress(mode, data, compression):
    if mode == 'b':
            maxVol = 2**15 - 1
            gainFromBytes(data, compression, maxVol)
    elif mode == 'f':
        compressWav(data, compression)


def gainFromBytes(curByte, compression, maxVol):
        if (int.from_bytes(curByte, "little") * compression) <= maxVol*50:
           return(struct.pack('<h', round(int.from_bytes(curByte, "little") * compression/100)))
        elif (int.from_bytes(curByte, "little") * compression) > maxVol*50 and (int.from_bytes(curByte, "little") * compression) < maxVol*100:
            return(struct.pack('<h', round(int.from_bytes(curByte, "little") / compression/100)))
        else:
            return(struct.pack('<h', maxVol))
            

def compressWav(filename, compression):

    wavRead = wave.open(filename,'rb')
    wavWrite = wave.open('I' + filename, 'wb')
    nFrames = wavRead.getnframes()

    maxVol = 2**((wavRead.getsampwidth() * 8)-1) - 1

    wavWrite.setnchannels(wavRead.getnchannels())
    wavWrite.setsampwidth(wavRead.getsampwidth())
    wavWrite.setframerate(wavRead.getframerate())

    for i in range(nFrames):
        wavWrite.writeframesraw(gainFromBytes(wavRead.readframes(1), compression, maxVol))

    wavRead.close()
    wavWrite.close()

    wavRead = wave.open('I' + filename,'rb')
    print(wavRead.readframes(wavRead.getnframes()), file=open('output2.txt', 'w'))
    wavRead.close()


if __name__ == "__main__":
    print("Enter file name")
    filename = 'Free_Test_Data_500KB_WAV.wav'
    print("Enter compression amount")
    c = input()
    c = round(float(c))*100
    compress('f', filename, c)