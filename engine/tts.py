import os
import wave
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def save_as_wav(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Wraps raw PCM data into a playable .wav file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

async def speak(text, output_file="response.wav"):
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-tts-preview", 
            contents=f"Please say this: {text}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Aoede') 
                    )
                )
            )
        )
        
        # Get the raw PCM bytes
        audio_part = response.candidates[0].content.parts[0]
        if hasattr(audio_part, 'inline_data'):
            raw_pcm_data = audio_part.inline_data.data
            
            # Save using our helper function to add the header
            save_as_wav(output_file, raw_pcm_data)
            
            # Now Windows Media Player or any app will recognize it!
            os.system(f"start {output_file}")
            
    except Exception as e:
        print(f"TTS Error: {e}")