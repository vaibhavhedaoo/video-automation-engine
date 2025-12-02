import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont

def create_subtitle_clip(text, duration, start_time, video_width, video_height):
    img = Image.new("RGBA", (video_width, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    w, h = draw.textsize(text, font=font)
    draw.text(((video_width - w) / 2, 20), text, font=font, fill="white")

    np_img = np.array(img)

    return (
        ImageClip(np_img)
        .set_duration(duration)
        .set_start(start_time)
        .set_position(("center", video_height * 0.75))
    )

def create_video(video_path, audio_path, output_path="final.mp4"):
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)
    music = AudioFileClip("assets/music/bg.mp3").volumex
