#!/bin/python3
# 标识引用的python版本
import pyaudio
import wave
import sys
import os
import numpy as np
"""
首先集成一下录音功能和格式转换功能
"""
class Record():
    """
    录音的类
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  
    CHANNELS = 1  声道
    RATE = 16000  频率
    RECORD_SECONDS = 5  录音时间  单位=> s
    WAVE_OUTPUT_FILENAME = os.getcwd() + "/python/output1.wav"   录音文件
    """
    def __init__(self,WAVE_OUTPUT_FILENAME='output1.wav',CHUNK=1024,
    FORMAT=pyaudio.paInt16,CHANNELS=1,RECORD_SECONDS=5,
    Input=True,RATE=16000,PCMName="out.pcm",DataType=np.int16):
        self.CHUNK = CHUNK
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RECORD_SECONDS = RECORD_SECONDS
        self.WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME
        self.Input = Input
        self.RATE = RATE
        self.PCMName = PCMName
        self.DataType = DataType
    
    def recording(self):
        """
        这句代码 会屏蔽一些不必要的报错
        os.close(sys.stderr.fileno())
        """
        #隐藏一些报错，这些不影响程序的运行
        os.close(sys.stderr.fileno())
        print("开始录音")
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK)
        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("done")
        # 关闭流
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        
        wf.close()

    def wav2pcm(self):
        """
        音频文件wav格式 转 pcm格式
        """
        f = open(self.WAVE_OUTPUT_FILENAME, "rb")
        f.seek(0)
        f.read(1024)
        data = np.fromfile(f, dtype=self.DataType)
        # 获取 分割后的 数组
        filePath =  str(self.WAVE_OUTPUT_FILENAME).split('/')
        path = ''
        # 拼接路径 取出最后一位 [0,-1)
        for item in filePath[:-1]:
            path += item +'/'
        path += self.PCMName 
        # print("PCM Path =>",path)
        data.tofile(path)
        print("结束")
        # 可以返回一个元组； 也可以把它封成数组返回
        return (self.WAVE_OUTPUT_FILENAME,path)

    def run(self):
        self.recording()
        wavpath,path = self.wav2pcm()
        #print("wave =>",wavpath,"\n","path =>",path)

    
# 这个就不写入那个类里了， 这样方便调用 不需要再初始化类了
# 可直接copy到使用的类中或者文件里
def pcm2wav(pcmfile,wavfile,channels=1,rate=16000):
    with open(pcmfile,'rb') as fp:
        pcmdata = fp.read()
    with wave.open(wavfile, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(16 // 8)
        wav.setframerate(rate)
            # 写入
        wav.writeframes(pcmdata)


# 测试
if __name__ == "__main__":
    wavepath = os.getcwd() + "/output1.wav"  
    dev = Record(wavepath)
    dev.run()
