import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------- FONT HELPER ----------

def get_font(size: int):
    """Try to use Anton font; fallback to default if something goes wrong."""
    try:
        return ImageFont.truetype("assets/fonts/anton.ttf", size)
    except Exception:
        return ImageFont.load_default()


# ---------- SUBTITLE RENDERING ----------

def create_subtitle_clip(text, duration, start_time, video_width, video_height):
    if not text.strip():
        return None

    # Subtitle area
    bar_height = 220
    img = Image.new("RGBA", (video_width, bar_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Semi-transparent dark bar
    overlay = Image.new("RGBA", (video_width, bar_height), (0, 0, 0, 120))
    img.alpha_composite(overlay)

    font = get_font(64)

    # Text sizing and centering
    w, h = draw.textsize(text, font=font)
    x = (video_width - w) // 2
    y = (bar_height - h) // 2

    # White text with slight black outline (for readability)
    draw.text(
        (x, y),
        text,
        font=font,
        fill="white",
        stroke_width=3,
        stroke_fill="black",
    )

    np_img = np.array(img)

    return (
        ImageClip(np_img)
        .set_duration(duration)
        .set_start(start_time)
        .set_position(("center", video_height * 0.78))  # slightly above bottom
        .crossfadein(0.2)
        .crossfadeout(0.2)
    )


# ---------- OUTRO HELPERS ----------

def blur_frame(image):
    pil_img = Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius=20))
    return np.array(pil_img)


def create_outro_text(text, video_width, video_height, duration):
    img = Image.new("RGBA", (video_width, video_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Semi-transparent center panel
    panel_width = int(video_width * 0.9)
    panel_height = int(video_height * 0.25)
    panel_x = (video_width - panel_width) // 2
    panel_y = (video_height - panel_height) // 2
    panel = Image.new("RGBA", (panel_width, panel_height), (0, 0, 0, 160))
    img.alpha_composite(panel, dest=(panel_x, panel_y))

    font = get_font(72)
    w, h = draw.textsize(text, font=font)
    x = (video_width - w) // 2
    y = (video_height - h) // 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill="white",
        stroke_width=3,
        stroke_fill="black",
    )

    np_img = np.array(img)
    return (
        ImageClip(np_img)
        .set_duration(duration)
        .set_position("center")
        .crossfadein(0.4)
        .crossfadeout(0.3)
    )


# ---------- MAIN VIDEO PIPELINE ----------

def create_video(video_path, audio_path, output_path="final.mp4"):
    print("DEBUG: Loading base video and audio...")
    video = VideoFileClip(video_path)
    voice = AudioFileClip(audio_path)

    # Lo-fi music (lower volume)
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.08)

    duration = voice.duration
    voice = voice.set_duration(duration).volumex(1.25)
    music = music.set_duration(duration)

    print("DEBUG: Reading script for subtitles...")
    with open("voice.txt", "r") as f:
        script_text = f.read().strip()

    # Dynamic subtitle chunks based on words
    words = script_text.split()
    chunk_size = 6  # ~6 words per subtitle
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ] or [script_text]

    num_chunks = len(chunks)
    segment_duration = duration / max(num_chunks, 1)

    print(f"DEBUG: Creating {num_chunks} subtitle clips...")
    subtitle_clips = []
    for i, chunk in enumerate(chunks):
        sub_clip = create_subtitle_clip(
            chunk,
            segment_duration,
            i * segment_duration,
            video.w,
            video.h,
        )
        if sub_clip:
            subtitle_clips.append(sub_clip)

    print("DEBUG: Adding logo overlay...")
    logo = (
        ImageClip("assets/logo/logo.png")
        .resize(width=200)
        .set_position(("right", "top"))
        .set_duration(duration)
    )

    print("DEBUG: Mixing audio (voice + music)...")
    final_audio = CompositeAudioClip([voice, music])

    # Outro timing
    outro_duration = min(2.5, duration * 0.3)
    outro_start = max(0, duration - outro_duration)

    print("DEBUG: Building outro clip...")
    outro_base = video.subclip(outro_start, duration).fl_image(blur_frame)

    outro_txt = create_outro_text(
        "Become 1% Better Every Day",
        video.w,
        video.h,
        outro_duration,
    )

    outro_logo = logo.copy().set_duration(outro_duration)

    outro_final = CompositeVideoClip([outro_base, outro_txt, outro_logo])

    print("DEBUG: Composing main body video...")
    body_video = (
        CompositeVideoClip([video] + subtitle_clips + [logo])
        .set_duration(outro_start)
        .set_audio(final_audio)
        .resize((1080, 1920))
    )

    outro_final = outro_final.resize((1080, 1920))

    print("DEBUG: Concatenating body + outro...")
    final = CompositeVideoClip([body_video, outro_final])

    print("DEBUG: Rendering final video to file...")
    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
    )

    print("DEBUG: Render complete:", output_path)
    return output_path
