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
    print("DEBUG: Loading video and audio files...")
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    duration = voice.duration
    music = music.set_duration(duration)
    voice = voice.set_duration(duration)

    print("DEBUG: Reading script text...")
    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    clips = []
    print("DEBUG: Creating subtitle clips...")
    for i, line in enumerate(lines):
        clips.append(create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h))

    print("DEBUG: Creating CompositeAudioClip...")
    final_audio = CompositeAudioClip([voice, music])
    print("DEBUG: CompositeAudioClip OK")

    print("DEBUG: Creating CompositeVideoClip...")
    final_video = CompositeVideoClip([video] + clips)
    final_video = final_video.set_audio(final_audio)
    final_video = final_video.resize((1080, 1920))
    print("DEBUG: CompositeVideoClip OK")

    print("DEBUG: Writing video file to disk...")
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    print("DEBUG: Video rendering finished!")
    return output_path
