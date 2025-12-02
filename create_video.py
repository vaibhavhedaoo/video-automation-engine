import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    CompositeAudioClip,
    TextClip,
    vfx
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
        .crossfadein(0.3)
        .crossfadeout(0.3)
    )

def create_video(video_path, audio_path, output_path="final.mp4"):
    print("DEBUG: Loading video and audio...")
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    duration = voice.duration
    music = music.set_duration(duration)
    voice = voice.set_duration(duration)

    print("DEBUG: Loading script...")
    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    clips = []
    print("DEBUG: Creating subtitle clips...")
    for i, line in enumerate(lines):
        clips.append(
            create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h)
        )

    # Logo overlay (top-right)
    print("DEBUG: Adding logo overlay...")
    logo = ImageClip("assets/logo/logo.png").resize(width=200)
    logo = logo.set_position(("right", "top")).set_duration(duration)

    print("DEBUG: Creating composite audio...")
    final_audio = CompositeAudioClip([voice, music])

    # Outro: blur last 2 seconds
    outro_duration = min(2, duration * 0.25)
    outro_clip = video.subclip(duration - outro_duration, duration).fx(vfx.blur, 25)

    outro_text = TextClip(
        "Become 1% Better Every Day",
        fontsize=70,
        color="white",
        method="caption",
        size=(900, None)
    ).set_position("center").set_duration(outro_duration).crossfadein(0.4)

    outro_final = CompositeVideoClip([outro_clip, outro_text, logo.copy()])

    print("DEBUG: Composing final video...")
    full_video = CompositeVideoClip([video] + clips + [logo]).set_audio(final_audio).resize((1080, 1920))

    print("DEBUG: Rendering combined video + outro...")
    final = CompositeVideoClip([full_video.set_duration(duration - outro_duration), outro_final])
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    print("DEBUG: Render complete!")
    return output_path
