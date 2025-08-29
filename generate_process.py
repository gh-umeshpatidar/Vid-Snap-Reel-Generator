import os
import time
import subprocess
from text_to_audio import text_to_speech_file
def text_to_audio(folder):
    with open(f"user_upload/{folder}/desc.txt") as f:
        text = f.read()
    
    if(text):
        text_to_speech_file(text,folder)
    else:
        with open(f"user_upload/{folder}/audio.txt") as f1:
           song = f1.read().strip()
        save_file_path = os.path.join(f"user_upload/{folder}",song)
        return save_file_path

def create_reel(folder,counter,audio):

    images_pattern = f"user_upload/{folder}/input.txt"
    audio_file = audio
    output_file = f"static/reels/{counter}.mp4"

    command = f'''ffmpeg -f concat -safe 0 -i {images_pattern} -i {audio_file} -vf "scale=1080:1920:force_original_aspect_ratio=decrease, pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p {output_file}'''
    subprocess.run(command,shell=True,check=True)

    

if __name__ == "__main__":
    while True:
        if not os.path.isfile("VidSnapAIProject/done.txt"):
            with open("done.txt", "w") as f:
                f.write("")
         
        with open("done.txt","r") as f:
            done_folder = f.readlines()
        
        done_folder = [f.strip() for  f in done_folder]
        folders = os.listdir("user_upload")
        new_found = False
        counter = 1
        for folder in folders:
            if(folder not in done_folder):
                new_found = True
                audio = text_to_audio(folder)
                print("**********",audio,"************")
                create_reel(folder,counter,audio)
                counter += 1
                with open("done.txt","a") as f:
                    f.write(folder + "\n")
        if not new_found:             
            break 
        
        time.sleep(5)
