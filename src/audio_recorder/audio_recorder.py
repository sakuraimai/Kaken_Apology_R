import pyaudio
import wave
import threading
import time
import sys
import os
from pygame import mixer


class AudioRecorder:
    def __init__(self, test_id, audio_input_channel):
        self.AUDIO_OUTPUT_DIR = os.getcwd() + "/results/wav"
        self.WAVE_OUTPUT_FILENAME = f"{str(test_id)}.wav"
        self.WAVE_OUTPUT_FILE_PATH = self.AUDIO_OUTPUT_DIR + "/" + self.WAVE_OUTPUT_FILENAME
        self.iDeviceIndex = audio_input_channel

        self.FORMAT = pyaudio.paInt16
        self.frames = []
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            input_device_index = self.iDeviceIndex,
                            frames_per_buffer=self.CHUNK, start=True)


    def start(self):
        def record():

            print("start recording...")

            while self.running:
                data = self.stream.read(self.CHUNK, exception_on_overflow = False)
                self.frames.append(data)
            sys.exit()

        mixer.init(frequency=44100)
        mixer.music.load("./src/audio_recorder/beep.mp3")
        mixer.music.set_volume(0.8)
        mixer.music.play()

        self.running = True
        self.thread = threading.Thread(target=record)
        self.thread.setDaemon(True)
        self.thread.start()

    def finish(self):
        self.running = False
        print("Recording stop")
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self._save_wav_file()

    def reset(self):
        self.running = False
        print("Recording stop")
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def _save_wav_file(self):
        waveFile = wave.open(self.WAVE_OUTPUT_FILE_PATH, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

        print("save wav file into wav dir")

    def wait(self, milisec):
        time.sleep(milisec/1000)