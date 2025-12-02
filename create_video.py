from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
import math

def create_video(video_path, audio_path, output_path="final.mp4"):

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    duration = audio.duration

    # background music
    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    # extract script text
    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    clips = []

    num_lines = len(lines)
    segment_duration = duration / max(num_lines, 1)

    y_position = video.h * 0.75  # subtitles lower area

    for i, line in enumerate(lines):
        subtitle = TextClip(
            line.strip(),
            fontsize=56,
            color='white',
            font="Arial-Bold"
        ).set_position(("center", y_position)).set_duration(segment_duration).set_start(i * segment_duration)
        clips.append(subtitle)

    final_audio = audio.volumex(1.0).audio_fadein(0.3).audio_fadeout(0.3).overlay(music)

    final_video = CompositeVideoClip([video] + clips)
    final_video = final_video.set_audio(final_audio)
    final_video = final_video.resize((1080, 1920))

    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path
