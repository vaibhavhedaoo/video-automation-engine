import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_subtitle_clip(text, duration, start_time, video_width, video_height):
    img = Image.new("RGBA", (video_width, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    draw.text(((video_width - w) / 2, 20), text, font=font, fill="white")
    return ImageClip(np.array(img)).set_duration(duration).set_start(start_time).set_position(("center", video_height * 0.75))

def blur_frame(image):
    pil_img = Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius=20))
    return np.array(pil_img)

def create_outro_text(text, video_width, video_height, duration):
    img = Image.new("RGBA", (video_width, video_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    draw.text(((video_width - w) / 2, (video_height - h) / 2), text, font=font, fill="white")
    return ImageClip(np.array(img)).set_duration(duration).set_position("center")

def create_video(video_path, audio_path, output_path="final.mp4"):
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    duration = voice.duration
    music = music.set_duration(duration)
    voice = voice.set_duration(duration)

    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    segment_duration = duration / max(len(lines), 1)

    clips = []
    for i, line in enumerate(lines):
        clips.append(create_subtitle_clip(line.strip(), segment_duration, i * segment_duration, video.w, video.h))

    logo = ImageClip("assets/logo/logo.png").resize(width=200).set_position(("right","top")).set_duration(duration)

    final_audio = CompositeAudioClip([voice, music])

    outro_duration = min(2, duration * 0.25)
    outro_clip = video.subclip(duration - outro_duration, duration).fl_image(blur_frame)

    outro_txt = create_outro_text("Become 1% Better Every Day", video.w, video.h, outro_duration)
    outro_final = CompositeVideoClip([outro_clip, outro_txt, logo.copy()])

    full_video = CompositeVideoClip([video] + clips + [logo]).set_audio(final_audio).resize((1080, 1920))
    final = CompositeVideoClip([full_video.set_duration(duration - outro_duration), outro_final])
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path
