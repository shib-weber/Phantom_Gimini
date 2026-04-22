import pyaudio
import wave
import numpy as np

def record_audio(filename="input.wav"):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    
    print("Phantom is listening...")
    frames = []
    silent_chunks = 0
    while True:
        data = stream.read(1024)
        frames.append(data)
        if np.abs(np.frombuffer(data, dtype=np.int16)).mean() < 500:
            silent_chunks += 1
        else:
            silent_chunks = 0
            
        if silent_chunks > 30: # Stop after ~2 seconds of silence
            break
            
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))