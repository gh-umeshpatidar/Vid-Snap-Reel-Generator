import os 
import uuid
from elevenlabs import VoiceSettings
from elevenlabs import ElevenLabs
from congi import API_KEY

client = ElevenLabs(
    api_key= API_KEY
)

def text_to_speech_file(text : str, folder : str) -> str:
   response = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_turbo_v2_5",
        output_format="mp3_22050_32",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
   )
   
   save_file_path = os.path.join(f"user_upload/{folder}","audio.mp3")

   with open(save_file_path,"wb") as f:
      for chunk in response:
         if chunk:
            f.write(chunk)

   print(f"{save_file_path} : a new audio file was saved successfully")
   
   return save_file_path 

# text_to_speech_file("save_file_path","myid")