import pyaudio
import wave

class Recorder:
    def __init__(self, file_path="data/recorded_audio.wav", duration=30, sample_rate=44100):
        self.file_path = file_path
        self.duration = duration
        self.sample_rate = sample_rate
        self.channels = 1
        self.chunk = 1024
        self.format = pyaudio.paInt16

    def record_audio(self):
        print(f"Recording audio for {self.duration} seconds...")
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)

        frames = []
        for _ in range(0, int(self.sample_rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        print("Record done.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        with wave.open(self.file_path, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved in: {self.file_path}")
