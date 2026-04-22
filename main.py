import asyncio
import time
import os
from utils.audio_utils import record_audio
from engine.stt import transcribe_audio
from engine.brain import generate_response
from engine.tts import speak

async def run_phantom():
    print("--- Phantom Online ---")
    
    # Path to the shared audio file
    audio_file = "input.wav"

    while True:
        # 1. Listen (Only starts once TTS is finished)
        print("\nPhantom is listening...")
        record_audio(audio_file)
        
        # 2. Transcribe
        text = transcribe_audio(audio_file)
        
        # Clean up the audio file immediately after transcription 
        # to prevent processing old data
        if os.path.exists(audio_file):
            os.remove(audio_file)

        if not text or len(text.strip()) < 2: 
            continue
            
        print(f"You: {text}")
        
        response = generate_response(text)
        print(f"Phantom: {response}")
        
 
        await speak(response)


        time.sleep(1.0)

if __name__ == "__main__":
    try:
        asyncio.run(run_phantom())
    except KeyboardInterrupt:
        print("\nPhantom: Shutting down. Goodbye!")