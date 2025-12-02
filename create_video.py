from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

def create_subtitle_clip(text, duration, start_time, video_width, video_height):
    font = ImageFont.load_default()  # Built-in font, works everywhere
    img = Image.new("RGBA", (video_width, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)
    draw.text(((video_width - w) / 2, 20), text, font=font, fill="white")

    return ImageClip(img).set_duration(duration).set_start(start_time).set_position(("center", video_height * 0.75))

def create_video(video_path, audio_path, output_path="final.mp4"):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    clips = []
    for i, line in enumerate(lines):
        clips.append(create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h))

    final_audio = audio.overlay(music)
    final_video = Com_
