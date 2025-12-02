from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video(video_path, audio_path, output_path="final.mp4"):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    duration = audio.duration

    music = AudioFileClip("assets/music/bg.mp3").volumex(0.15)

    with open("voice.txt", "r") as f:
        script_text = f.read()

    lines = script_text.split(". ")
    clips = []

    num_lines = len(lines)
    segment_duration = duration / max(num_lines, 1)

    y_position = video.h * 0.75

    for i, line in enumerate(lines):
        subtitle = TextClip(
            txt=line.strip(),
            fontsize=64,
            color="white",
            method='label'  # <- Pillow backend
        ).set_position(("center", y_position)).set_duration(segment_duration).set_start(i * segment_duration)
        clips.append(subtitle)

    final_audio = audio.overlay(music)

    final_video = CompositeVideoClip([video] + clips)
    final_video = final_video.set_audio(final_audio)
    final_video = final_video.resize((1080, 1920))

    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    return output_path
