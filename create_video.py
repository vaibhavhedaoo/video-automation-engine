from moviepy.editor import *
import os

def create_video(bg_path, voice_path, output="final.mp4"):
    audio = AudioFileClip(voice_path)
    clip = VideoFileClip(bg_path).subclip(0, audio.duration)
    clip = clip.resize((1080, 1920))
    final = clip.set_audio(audio)
    final.write_videofile(output, fps=30)
    return output
