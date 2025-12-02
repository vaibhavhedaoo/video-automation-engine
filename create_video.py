from moviepy.editor import VideoFileClip, AudioFileClip

def create_video(video_path, audio_path, output_path="final.mp4"):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    final = video.set_audio(audio)
    final = final.resize((1080, 1920))

    final.write_videofile(output_path, fps=30)
    return output_path
