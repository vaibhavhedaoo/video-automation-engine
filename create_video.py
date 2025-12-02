import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont

def create_subtitle_clip(text, duration, start_time, video_width, video_height):
    # Create transparent image for subtitle background
    img = Image.new("RGBA", (video_width, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Use built-in Pillow font (works without external font files)
    font = ImageFont.load_default()

    # Calculate text size and apply centered drawing
    w, h = draw.textsize(text, font=font)
    draw.text(((video_width - w) / 2, 20), text, font=font, fill="white")

    # Convert image to numpy array for ImageClip
    np_img = np.array(img)

    # Create subtitle clip
    return (
        ImageClip(np_img)
        .set_duration(duration)
        .set_start(start_time)
        .set_position(("center", video_height * 0.75))  # Bottom center
    )

def create_video(video_path, audio_path, output_path="final.mp4"):
    # Load main background video and voice audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Add background music
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    # Load script from saved file
    with open("voice.txt", "r") as f:
        script_text = f.read()

    # Split script into lines for subtitles
    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    # Create subtitle clip list
    clips = []
    for i, line in enumerate(lines):
        clips.append(create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h))

    # Mix audio tracks
    final_audio = audio.overlay(music)

    # Combine video + subtitles
    final_video = CompositeVideoClip([video] + clips)
    final_video = final_video.set_audio(final_audio)
    final_video = final_video.resize((1080, 1920))

    # Render final video
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path
