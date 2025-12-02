import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    CompositeAudioClip,
    TextClip
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

def blur_frame(image):
    pil_img = Image.fromarray(image)
    pil_img = pil_img.filter(ImageFilter.GaussianBlur(radius=20))
    return np.array(pil_img)

def create_video(video_path, audio_path, output_path="final.mp4"):
    print("DEBUG: Loading inputs...")
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    duration = voice.duration
    music = music.set_duration(duration)
    voice = voice.set_duration(duration)

    print("DEBUG: Reading script...")
    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    clips = []
    print("DEBUG: Building subtitles...")
    for i, line in enumerate(lines):
        clips.append(create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h))

    print("DEBUG: Adding logo...")
    logo = ImageClip("assets/logo/logo.png").resize(width=200)
    logo = logo.set_position(("right", "top")).set_duration(duration)

    print("DEBUG: Composing audio...")
    final_audio = CompositeAudioClip([voice, music])

    print("DEBUG: Creating outro...")
    outro_duration = min(2, duration * 0.25)
    outro_clip = video.subclip(duration - outro_duration, duration).fl_image(blur_frame)

    outro_text = TextClip(
        "Become 1% Better Every Day",
        fontsize=70,
        color="white",
        method="caption",
        size=(900, None)
    ).set_position("center").set_duration(outro_duration).crossfadein(0.4)

    outro_final = CompositeVideoClip([outro_clip, outro_text, logo.copy()])

    print("DEBUG: Combining video...")
    full_video = CompositeVideoClip([video] + clips + [logo]).set_audio(final_audio).resize((1080, 1920))

    print("DEBUG: Rendering final video...")
    final = CompositeVideoClip([full_video.set_duration(duration - outro_duration), outro_final])
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    print("DEBUG: Done rendering!")
    return output_path
